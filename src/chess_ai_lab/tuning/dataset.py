from __future__ import annotations

import hashlib
import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
import time

import chess
import numpy as np
import pyarrow.parquet as pq

from chess_ai_lab.evaluation.features import FEATURES
from chess_ai_lab.tuning.position import TrainingPosition


@dataclass(slots=True)
class TrainingBatch:
    """
    学習用の1バッチ。

    feature_matrix:
        shape = (batch_size, feature_count)

    target_cps:
        shape = (batch_size,)

    source_depths:
        shape = (batch_size,)

    positions:
        feature_values が存在しない旧形式データ用。
    """

    feature_matrix: np.ndarray | None
    target_cps: np.ndarray
    source_depths: np.ndarray
    positions: list[TrainingPosition] | None = None

    @property
    def size(self) -> int:
        return len(self.target_cps)


class ParquetDataset:
    """
    Parquetから学習データを読み込む。

    初回アクセス時にParquet全体をNumPyへ読み込み、
    以後はメモリ上のキャッシュを使用する。

    これにより、

        Epoch 1: Parquet読み込み
        Epoch 2: キャッシュ
        Epoch 3: キャッシュ
        ...

    となり、同じデータを毎epochディスクから
    読み直すことを防ぐ。
    """

    def __init__(
        self,
        path: str | Path,
        batch_size: int = 4096,
    ):
        self._path = Path(path)
        self._batch_size = batch_size

        # -------------------------
        # Memory cache
        # -------------------------

        self._feature_matrix: np.ndarray | None = None
        self._target_cps: np.ndarray | None = None
        self._source_depths: np.ndarray | None = None

        self._positions: list[TrainingPosition] | None = None

        self._loaded = False

    @staticmethod
    def _current_feature_names() -> list[str]:
        return [
            name
            for name, _ in FEATURES
        ]

    @classmethod
    def _current_feature_schema_hash(cls) -> str:
        canonical = json.dumps(
            cls._current_feature_names(),
            ensure_ascii=False,
            separators=(",", ":"),
        )

        return hashlib.sha256(
            canonical.encode("utf-8")
        ).hexdigest()

    def _validate_feature_metadata(
        self,
        parquet: pq.ParquetFile,
    ) -> None:
        metadata = parquet.schema_arrow.metadata

        if metadata is None:
            raise ValueError(
                f"Parquet dataset has no schema metadata: "
                f"{self._path}"
            )

        feature_names_raw = metadata.get(
            b"chess_ai_lab.feature_names"
        )

        feature_count_raw = metadata.get(
            b"chess_ai_lab.feature_count"
        )

        feature_schema_hash_raw = metadata.get(
            b"chess_ai_lab.feature_schema_hash"
        )

        if (
            feature_names_raw is None
            or feature_count_raw is None
            or feature_schema_hash_raw is None
        ):
            raise ValueError(
                "Parquet dataset is missing required "
                "Feature Registry metadata: "
                f"{self._path}"
            )

        try:
            dataset_feature_names = json.loads(
                feature_names_raw.decode("utf-8")
            )

            dataset_feature_count = int(
                feature_count_raw.decode("utf-8")
            )

            dataset_feature_schema_hash = (
                feature_schema_hash_raw.decode("utf-8")
            )

        except (
            UnicodeDecodeError,
            ValueError,
            TypeError,
            json.JSONDecodeError,
        ) as exc:
            raise ValueError(
                "Invalid Feature Registry metadata in "
                f"{self._path}"
            ) from exc

        current_feature_names = (
            self._current_feature_names()
        )

        current_feature_count = len(
            current_feature_names
        )

        current_feature_schema_hash = (
            self._current_feature_schema_hash()
        )

        if dataset_feature_count != current_feature_count:
            raise ValueError(
                "Feature count mismatch.\n"
                f"Dataset: {dataset_feature_count}\n"
                f"Current: {current_feature_count}\n"
                f"Path: {self._path}"
            )

        if dataset_feature_names != current_feature_names:
            raise ValueError(
                "Feature Registry order/name mismatch.\n"
                f"Dataset: {dataset_feature_names}\n"
                f"Current: {current_feature_names}\n"
                f"Path: {self._path}"
            )

        if (
            dataset_feature_schema_hash
            != current_feature_schema_hash
        ):
            raise ValueError(
                "Feature schema hash mismatch.\n"
                f"Dataset: {dataset_feature_schema_hash}\n"
                f"Current: {current_feature_schema_hash}\n"
                f"Path: {self._path}"
            )

    def _load_into_memory(self) -> None:
        """
        Parquet全体をメモリへ読み込む。

        初回のiter_batches()からのみ呼ばれる。
        """

        if self._loaded:
            return

        start = time.perf_counter()

        print(f"Loading Parquet into memory: {self._path}")

        parquet = pq.ParquetFile(self._path)

        self._validate_feature_metadata(parquet)

        # --------------------------------
        # feature_values がある新形式
        # --------------------------------

        feature_batches: list[np.ndarray] = []
        target_batches: list[np.ndarray] = []
        depth_batches: list[np.ndarray] = []

        # --------------------------------
        # 旧形式用
        # --------------------------------

        positions: list[TrainingPosition] = []

        has_feature_values: bool | None = None

        total_rows = 0

        for batch in parquet.iter_batches(
            batch_size=self._batch_size,
        ):
            table = batch.to_pydict()

            target_cps = np.asarray(
                table["target_cp"],
                dtype=np.float64,
            )

            source_depths = np.asarray(
                table["source_depth"],
                dtype=np.int32,
            )

            feature_values = table.get(
                "feature_values"
            )

            # --------------------------------
            # 新形式
            # --------------------------------

            if feature_values is not None:

                if has_feature_values is False:
                    raise ValueError(
                        "Parquet dataset contains "
                        "mixed feature formats."
                    )

                has_feature_values = True

                feature_matrix = np.asarray(
                    feature_values,
                    dtype=np.float64,
                )

                if feature_matrix.ndim != 2:
                    raise ValueError(
                        "feature_values must be a "
                        "2-dimensional array."
                    )

                expected_feature_count = len(
                    FEATURES
                )

                if (
                    feature_matrix.shape[1]
                    != expected_feature_count
                ):
                    raise ValueError(
                        "Feature vector dimension mismatch.\n"
                        f"Dataset: "
                        f"{feature_matrix.shape[1]}\n"
                        f"Current: "
                        f"{expected_feature_count}\n"
                        f"Path: {self._path}"
                    )

                feature_batches.append(
                    feature_matrix
                )

                target_batches.append(
                    target_cps
                )

                depth_batches.append(
                    source_depths
                )

                total_rows += len(target_cps)

            # --------------------------------
            # 旧形式
            # --------------------------------

            else:

                if has_feature_values is True:
                    raise ValueError(
                        "Parquet dataset contains "
                        "mixed feature formats."
                    )

                has_feature_values = False

                fens = table["fen"]

                for fen, cp, depth in zip(
                    fens,
                    table["target_cp"],
                    table["source_depth"],
                ):
                    positions.append(
                        TrainingPosition(
                            board=chess.Board(fen),
                            target_cp=cp,
                            source_depth=depth,
                            feature_values=None,
                        )
                    )

                total_rows += len(fens)

        # --------------------------------
        # Cache construction
        # --------------------------------

        if has_feature_values is True:

            if not feature_batches:
                raise ValueError(
                    "Parquet dataset contains no rows."
                )

            self._feature_matrix = np.concatenate(
                feature_batches,
                axis=0,
            )

            self._target_cps = np.concatenate(
                target_batches,
                axis=0,
            )

            self._source_depths = np.concatenate(
                depth_batches,
                axis=0,
            )

            self._positions = None

        elif has_feature_values is False:

            if not positions:
                raise ValueError(
                    "Parquet dataset contains no rows."
                )

            self._feature_matrix = None
            self._target_cps = np.asarray(
                [
                    position.target_cp
                    for position in positions
                ],
                dtype=np.float64,
            )

            self._source_depths = np.asarray(
                [
                    position.source_depth
                    for position in positions
                ],
                dtype=np.int32,
            )

            self._positions = positions

        else:
            raise ValueError(
                "Parquet dataset contains no rows."
            )

        self._loaded = True

        elapsed = (
            time.perf_counter() - start
        )

        print(
            f"Dataset cached: "
            f"{total_rows:,} samples "
            f"in {elapsed:.3f} sec"
        )

    def iter_batches(self) -> Iterator[TrainingBatch]:
        """
        学習データをTrainingBatch単位で返す。

        初回:
            Parquet -> NumPy cache

        2回目以降:
            NumPy cache -> TrainingBatch
        """

        self._load_into_memory()

        if self._feature_matrix is not None:

            total = len(
                self._target_cps
            )

            for start in range(
                0,
                total,
                self._batch_size,
            ):
                end = min(
                    start + self._batch_size,
                    total,
                )

                yield TrainingBatch(
                    feature_matrix=(
                        self._feature_matrix[
                            start:end
                        ]
                    ),
                    target_cps=(
                        self._target_cps[
                            start:end
                        ]
                    ),
                    source_depths=(
                        self._source_depths[
                            start:end
                        ]
                    ),
                )

        else:

            if self._positions is None:
                raise RuntimeError(
                    "Dataset cache is invalid."
                )

            total = len(
                self._positions
            )

            for start in range(
                0,
                total,
                self._batch_size,
            ):
                end = min(
                    start + self._batch_size,
                    total,
                )

                batch_positions = (
                    self._positions[
                        start:end
                    ]
                )

                yield TrainingBatch(
                    feature_matrix=None,
                    target_cps=(
                        self._target_cps[
                            start:end
                        ]
                    ),
                    source_depths=(
                        self._source_depths[
                            start:end
                        ]
                    ),
                    positions=batch_positions,
                )

    def __iter__(self) -> Iterator[TrainingPosition]:
        """
        既存コードとの互換性を維持する。

        バッチ化された内部処理を、
        必要な場合だけTrainingPositionへ展開する。
        """

        for batch in self.iter_batches():

            if batch.feature_matrix is not None:

                for i in range(batch.size):

                    yield TrainingPosition(
                        board=None,
                        target_cp=int(
                            batch.target_cps[i]
                        ),
                        source_depth=int(
                            batch.source_depths[i]
                        ),
                        feature_values=(
                            batch.feature_matrix[i]
                        ),
                    )

            else:

                if batch.positions is None:
                    raise RuntimeError(
                        "TrainingBatch.positions is None."
                    )

                yield from batch.positions
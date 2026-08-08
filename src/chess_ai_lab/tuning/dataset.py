from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
import time

import chess
import numpy as np
import pyarrow.parquet as pq

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
    Parquetから学習データをバッチ単位で読み込む。
    """

    def __init__(
        self,
        path: str | Path,
        batch_size: int = 4096,
    ):
        self._path = Path(path)
        self._batch_size = batch_size

    def iter_batches(self) -> Iterator[TrainingBatch]:
        """
        学習データをTrainingBatch単位で返す。
        """

        start = time.perf_counter()

        print(f"Opening Parquet: {self._path}")

        parquet = pq.ParquetFile(self._path)

        print(
            f"Parquet opened in "
            f"{time.perf_counter() - start:.3f} sec"
        )

        batch_index = 0

        for batch in parquet.iter_batches(
            batch_size=self._batch_size,
        ):
            if batch_index == 0:
                print(
                    f"First batch loaded in "
                    f"{time.perf_counter() - start:.3f} sec"
                )

            table = batch.to_pydict()

            if batch_index == 0:
                print(
                    f"First batch converted in "
                    f"{time.perf_counter() - start:.3f} sec"
                )

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

            if feature_values is not None:

                feature_matrix = np.asarray(
                    feature_values,
                    dtype=np.float64,
                )

                if feature_matrix.ndim != 2:
                    raise ValueError(
                        "feature_values must be a "
                        "2-dimensional array."
                    )

                if batch_index == 0:
                    print(
                        f"First sample ready in "
                        f"{time.perf_counter() - start:.3f} sec"
                    )

                yield TrainingBatch(
                    feature_matrix=feature_matrix,
                    target_cps=target_cps,
                    source_depths=source_depths,
                )

            else:
                fens = table["fen"]

                positions: list[TrainingPosition] = []

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

                if batch_index == 0:
                    print(
                        f"First sample ready in "
                        f"{time.perf_counter() - start:.3f} sec"
                    )

                yield TrainingBatch(
                    feature_matrix=None,
                    target_cps=target_cps,
                    source_depths=source_depths,
                    positions=positions,
                )

            batch_index += 1

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
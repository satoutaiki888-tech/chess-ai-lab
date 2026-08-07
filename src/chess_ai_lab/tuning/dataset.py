from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
import time

import chess
import pyarrow.parquet as pq

from chess_ai_lab.tuning.position import TrainingPosition


class ParquetDataset:
    """
    Parquetから学習データをストリーミングで読み込む。
    """

    def __init__(
        self,
        path: str | Path,
        batch_size: int = 4096,
    ):
        self._path = Path(path)
        self._batch_size = batch_size

    def __iter__(self) -> Iterator[TrainingPosition]:
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

            fens = table["fen"]
            cps = table["target_cp"]
            depths = table["source_depth"]

            for i, (fen, cp, depth) in enumerate(
                zip(fens, cps, depths)
            ):
                if batch_index == 0 and i == 0:
                    print(
                        f"First sample ready in "
                        f"{time.perf_counter() - start:.3f} sec"
                    )

                yield TrainingPosition(
                    board=chess.Board(fen),
                    target_cp=cp,
                    source_depth=depth,
                )

            batch_index += 1
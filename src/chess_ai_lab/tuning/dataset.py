from __future__ import annotations

from pathlib import Path
from typing import Iterator

import pyarrow.parquet as pq

import chess

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
        parquet = pq.ParquetFile(self._path)

        for batch in parquet.iter_batches(
            batch_size=self._batch_size,
        ):
            table = batch.to_pydict()

            fens = table["fen"]
            cps = table["target_cp"]
            depths = table["source_depth"]

            for fen, cp, depth in zip(
                fens,
                cps,
                depths,
            ):
                yield TrainingPosition(
                    board=chess.Board(fen),
                    target_cp=cp,
                    source_depth=depth,
                )
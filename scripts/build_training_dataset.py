from __future__ import annotations

import argparse
from pathlib import Path
from datasets import load_dataset
import random

import pyarrow as pa
import pyarrow.parquet as pq

class ParquetStreamWriter:
    """
    Parquetへ逐次書き込む。
    """

    def __init__(self, path: Path):
        self.path = path
        self.writer: pq.ParquetWriter | None = None

    def write(self, rows: list[dict]) -> None:
        if not rows:
            return

        table = pa.Table.from_pylist(rows)

        if self.writer is None:
            self.writer = pq.ParquetWriter(
                self.path,
                table.schema,
                compression="zstd",
            )

        self.writer.write_table(table)

    def close(self) -> None:
        if self.writer is not None:
            self.writer.close()
            
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build Texel training dataset."
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory.",
    )

    parser.add_argument(
        "--max-samples",
        type=int,
        default=100_000,
        help="Maximum number of positions.",
    )

    parser.add_argument(
        "--min-depth",
        type=int,
        default=20,
        help="Minimum Stockfish depth.",
    )

    parser.add_argument(
        "--cp-limit",
        type=int,
        default=1000,
        help="Clamp centipawn score.",
    )

    parser.add_argument(
        "--train-ratio",
        type=float,
        default=0.9,
        help="Train dataset ratio.",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed.",
    )
    
    parser.add_argument(
        "--buffer-size",
        type=int,
        default=5000,
        help="Rows written per Parquet flush.",
    )

    return parser.parse_args()
def process_position(
    row: dict,
    *,
    min_depth: int,
    cp_limit: int,
) -> dict | None:
    """
    学習用に局面を前処理する。

    条件を満たさない局面は None を返す。
    """

    # mate局面は除外
    if row["mate"] is not None:
        return None

    # 深さ不足は除外
    if row["depth"] < min_depth:
        return None

    cp = max(
        -cp_limit,
        min(cp_limit, row["cp"]),
    )

    return {
        "fen": row["fen"],
        "target_cp": cp,
        "source_depth": row["depth"],
    }
    
def main() -> None:
    args = parse_args()

    args.output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataset = load_dataset(
        "Lichess/chess-position-evaluations",
        split="train",
        streaming=True,
    )

    rng = random.Random(args.seed)

    train_path = args.output_dir / "train.parquet"
    valid_path = args.output_dir / "valid.parquet"

    train_writer = None
    valid_writer = None

    train_buffer: list[dict] = []
    valid_buffer: list[dict] = []

    collected = 0
    train_count = 0
    valid_count = 0

    def flush_train() -> None:
        nonlocal train_writer, train_count

        if not train_buffer:
            return

        table = pa.Table.from_pylist(train_buffer)

        if train_writer is None:
            train_writer = pq.ParquetWriter(
                train_path,
                table.schema,
                compression="zstd",
            )

        train_writer.write_table(table)

        train_count += len(train_buffer)

        train_buffer.clear()

    def flush_valid() -> None:
        nonlocal valid_writer, valid_count

        if not valid_buffer:
            return

        table = pa.Table.from_pylist(valid_buffer)

        if valid_writer is None:
            valid_writer = pq.ParquetWriter(
                valid_path,
                table.schema,
                compression="zstd",
            )

        valid_writer.write_table(table)

        valid_count += len(valid_buffer)

        valid_buffer.clear()

    try:
        for row in dataset:

            sample = process_position(
                row,
                min_depth=args.min_depth,
                cp_limit=args.cp_limit,
            )

            if sample is None:
                continue

            collected += 1

            if rng.random() < args.train_ratio:
                train_buffer.append(sample)

                if len(train_buffer) >= args.buffer_size:
                    flush_train()

            else:
                valid_buffer.append(sample)

                if len(valid_buffer) >= args.buffer_size:
                    flush_valid()

            if collected >= args.max_samples:
                break

        flush_train()
        flush_valid()

    finally:

        if train_writer is not None:
            train_writer.close()

        if valid_writer is not None:
            valid_writer.close()

    print(f"Collected : {collected:,}")
    print(f"Train     : {train_count:,}")
    print(f"Valid     : {valid_count:,}")
    
if __name__ == "__main__":
    main()
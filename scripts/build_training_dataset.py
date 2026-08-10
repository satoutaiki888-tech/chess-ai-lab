from __future__ import annotations

import argparse
import hashlib
import json
import random
import time
from pathlib import Path

from datasets import load_dataset
import pyarrow as pa
import pyarrow.parquet as pq
import chess

from chess_ai_lab.evaluation.evaluator import Evaluator
from chess_ai_lab.evaluation.features import FEATURES


def build_feature_metadata() -> dict[bytes, bytes]:
    """
    現在のFeature Registry情報をParquet metadata用に生成する。
    """

    feature_names = [
        name
        for name, _ in FEATURES
    ]

    canonical = json.dumps(
        feature_names,
        ensure_ascii=False,
        separators=(",", ":"),
    )

    feature_schema_hash = hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()

    return {
        b"chess_ai_lab.feature_names": (
            canonical.encode("utf-8")
        ),
        b"chess_ai_lab.feature_count": str(
            len(feature_names)
        ).encode("utf-8"),
        b"chess_ai_lab.feature_schema_hash": (
            feature_schema_hash.encode("utf-8")
        ),
    }


def build_dataset_manifest(
    *,
    args: argparse.Namespace,
    collected: int,
    train_count: int,
    valid_count: int,
) -> dict:
    """生成したDatasetの再現条件と実績を記録する。"""

    feature_names = [
        name
        for name, _ in FEATURES
    ]

    canonical = json.dumps(
        feature_names,
        ensure_ascii=False,
        separators=(",", ":"),
    )

    feature_schema_hash = hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()

    return {
        "dataset_format_version": 1,
        "source": "Lichess/chess-position-evaluations",
        "split": "train",
        "max_samples": args.max_samples,
        "actual_samples": collected,
        "train_samples": train_count,
        "validation_samples": valid_count,
        "min_depth": args.min_depth,
        "cp_limit": args.cp_limit,
        "train_ratio": args.train_ratio,
        "actual_train_ratio": (
            train_count / collected
            if collected
            else 0.0
        ),
        "seed": args.seed,
        "buffer_size": args.buffer_size,
        "feature_names": feature_names,
        "feature_count": len(feature_names),
        "feature_schema_hash": feature_schema_hash,
    }


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
        default=1_000_000,
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

    parser.add_argument(
        "--progress-interval",
        type=int,
        default=100_000,
        help="Print progress every N collected samples.",
    )

    args = parser.parse_args()

    if args.max_samples <= 0:
        parser.error("--max-samples must be greater than 0.")

    if args.min_depth < 0:
        parser.error("--min-depth must be non-negative.")

    if args.cp_limit <= 0:
        parser.error("--cp-limit must be greater than 0.")

    if not 0.0 < args.train_ratio < 1.0:
        parser.error("--train-ratio must be between 0 and 1.")

    if args.buffer_size <= 0:
        parser.error("--buffer-size must be greater than 0.")

    if args.progress_interval <= 0:
        parser.error("--progress-interval must be greater than 0.")

    return args


def process_position(
    row: dict,
    *,
    evaluator: Evaluator,
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

    board = chess.Board(row["fen"])

    snapshot = evaluator.snapshot(board)

    return {
        "fen": row["fen"],
        "target_cp": cp,
        "source_depth": row["depth"],
        "feature_values": snapshot.feature_vector.tolist(),
    }


def apply_feature_metadata(
    table: pa.Table,
) -> pa.Table:
    """
    Parquet schema metadataへFeature Registry情報を付与する。
    """

    metadata = dict(table.schema.metadata or {})
    metadata.update(build_feature_metadata())

    return table.replace_schema_metadata(metadata)


def write_table(
    writer: pq.ParquetWriter | None,
    path: Path,
    rows: list[dict],
) -> pq.ParquetWriter:
    """
    rowsをParquetへ書き込む。

    最初のTableにFeature metadataを付与し、
    そのschemaをParquetWriterで固定する。
    """

    table = pa.Table.from_pylist(rows)

    table = apply_feature_metadata(table)

    if writer is None:
        writer = pq.ParquetWriter(
            path,
            table.schema,
            compression="zstd",
        )

    writer.write_table(table)

    return writer


def main() -> None:
    args = parse_args()

    evaluator = Evaluator()

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
    manifest_path = args.output_dir / "dataset.json"

    train_writer: pq.ParquetWriter | None = None
    valid_writer: pq.ParquetWriter | None = None

    train_buffer: list[dict] = []
    valid_buffer: list[dict] = []

    collected = 0
    train_count = 0
    valid_count = 0
    started_at = time.perf_counter()
    next_progress = args.progress_interval

    def flush_train() -> None:
        nonlocal train_writer, train_count

        if not train_buffer:
            return

        train_writer = write_table(
            train_writer,
            train_path,
            train_buffer,
        )

        train_count += len(train_buffer)

        train_buffer.clear()

    def flush_valid() -> None:
        nonlocal valid_writer, valid_count

        if not valid_buffer:
            return

        valid_writer = write_table(
            valid_writer,
            valid_path,
            valid_buffer,
        )

        valid_count += len(valid_buffer)

        valid_buffer.clear()

    try:
        for row in dataset:

            sample = process_position(
                row,
                evaluator=evaluator,
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

            if collected >= next_progress:
                elapsed = time.perf_counter() - started_at
                print(
                    f"Progress  : {collected:,} samples "
                    f"({elapsed:.1f} sec)"
                )
                next_progress += args.progress_interval

            if collected >= args.max_samples:
                break

        flush_train()
        flush_valid()

    finally:

        if train_writer is not None:
            train_writer.close()

        if valid_writer is not None:
            valid_writer.close()

    manifest = build_dataset_manifest(
        args=args,
        collected=collected,
        train_count=train_count,
        valid_count=valid_count,
    )

    manifest_path.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print(f"Collected : {collected:,}")
    print(f"Train     : {train_count:,}")
    print(f"Valid     : {valid_count:,}")
    print(f"Manifest  : {manifest_path}")


if __name__ == "__main__":
    main()

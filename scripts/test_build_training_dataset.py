from __future__ import annotations
import numpy as np
import argparse
import json

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from build_training_dataset import (
    apply_feature_metadata,
    build_dataset_manifest,
    build_feature_metadata,
    parse_args,
    process_position,
    write_table,
)


class _Snapshot:
    def __init__(self) -> None:
        self.feature_vector = np.array(
            [0.1, -0.2, 0.3],
            dtype=np.float64,
        )


class _Evaluator:
    def snapshot(self, board):
        return _Snapshot()


def test_parse_args_defaults(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "sys.argv",
        [
            "build_training_dataset.py",
            "--output-dir",
            str(tmp_path),
        ],
    )

    args = parse_args()

    assert args.output_dir == tmp_path
    assert args.max_samples == 1_000_000
    assert args.min_depth == 20
    assert args.cp_limit == 1000
    assert args.train_ratio == 0.9
    assert args.seed == 42
    assert args.buffer_size == 5000
    assert args.progress_interval == 100_000


def test_parse_args_rejects_invalid_max_samples(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(
        "sys.argv",
        [
            "build_training_dataset.py",
            "--output-dir",
            str(tmp_path),
            "--max-samples",
            "0",
        ],
    )

    with pytest.raises(SystemExit):
        parse_args()


def test_process_position_filters_mate_and_depth():
    evaluator = _Evaluator()

    # Mate position must be excluded.
    assert process_position(
        {
            "fen": "8/8/8/8/8/8/8/K6k w - - 0 1",
            "mate": 1,
            "depth": 30,
            "cp": 50,
        },
        evaluator=evaluator,
        min_depth=20,
        cp_limit=1000,
    ) is None

    # Position below minimum depth must be excluded.
    assert process_position(
        {
            "fen": "8/8/8/8/8/8/8/K6k w - - 0 1",
            "mate": None,
            "depth": 19,
            "cp": 50,
        },
        evaluator=evaluator,
        min_depth=20,
        cp_limit=1000,
    ) is None


def test_process_position_clamps_cp_and_serializes_features():
    sample = process_position(
        {
            "fen": "8/8/8/8/8/8/8/K6k w - - 0 1",
            "mate": None,
            "depth": 25,
            "cp": 5000,
        },
        evaluator=_Evaluator(),
        min_depth=20,
        cp_limit=1000,
    )

    assert sample is not None
    assert sample["target_cp"] == 1000
    assert sample["source_depth"] == 25
    assert sample["feature_values"] == [
        0.1,
        -0.2,
        0.3,
    ]


def test_feature_metadata_is_attached_to_parquet_schema():
    table = pa.Table.from_pylist(
        [
            {
                "fen": "x",
                "target_cp": 10,
                "source_depth": 20,
            }
        ]
    )

    result = apply_feature_metadata(table)

    metadata = result.schema.metadata
    expected = build_feature_metadata()

    assert metadata is not None

    for key, value in expected.items():
        assert metadata[key] == value


def test_write_table_creates_readable_parquet_with_metadata(
    tmp_path,
):
    path = tmp_path / "train.parquet"

    rows = [
        {
            "fen": "fen-1",
            "target_cp": 100,
            "source_depth": 20,
            "feature_values": [
                0.1,
                0.2,
                0.3,
            ],
        },
        {
            "fen": "fen-2",
            "target_cp": -50,
            "source_depth": 25,
            "feature_values": [
                0.4,
                0.5,
                0.6,
            ],
        },
    ]

    writer = write_table(
        None,
        path,
        rows,
    )
    writer.close()

    table = pq.read_table(path)

    assert table.num_rows == 2

    assert table.column_names == [
        "fen",
        "target_cp",
        "source_depth",
        "feature_values",
    ]

    assert table.schema.metadata is not None

    assert (
        b"chess_ai_lab.feature_schema_hash"
        in table.schema.metadata
    )


def test_manifest_records_generation_conditions_and_counts(
    tmp_path,
):
    args = argparse.Namespace(
        max_samples=1_000_000,
        min_depth=20,
        cp_limit=1000,
        train_ratio=0.9,
        seed=42,
        buffer_size=5000,
    )

    manifest = build_dataset_manifest(
        args=args,
        collected=1000,
        train_count=897,
        valid_count=103,
    )

    assert manifest["dataset_format_version"] == 1
    assert manifest["max_samples"] == 1_000_000
    assert manifest["actual_samples"] == 1000
    assert manifest["train_samples"] == 897
    assert manifest["validation_samples"] == 103

    assert manifest["actual_train_ratio"] == pytest.approx(
        0.897
    )

    assert manifest["min_depth"] == 20
    assert manifest["cp_limit"] == 1000
    assert manifest["seed"] == 42

    assert (
        manifest["feature_count"]
        == len(manifest["feature_names"])
    )

    assert len(
        manifest["feature_schema_hash"]
    ) == 64

    output = tmp_path / "dataset.json"

    output.write_text(
        json.dumps(manifest),
        encoding="utf-8",
    )

    restored = json.loads(
        output.read_text(encoding="utf-8")
    )

    assert restored == manifest
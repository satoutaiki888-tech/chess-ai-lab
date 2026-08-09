from __future__ import annotations

import json

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from chess_ai_lab.tuning.dataset import ParquetDataset


def _write_dataset(
    path,
    *,
    feature_names: list[str],
    feature_count: int,
    feature_schema_hash: str,
) -> None:
    rows = [
        {
            "fen": "8/8/8/8/8/8/8/K6k w - - 0 1",
            "target_cp": 0,
            "source_depth": 20,
            "feature_values": [0.0] * feature_count,
        }
    ]

    table = pa.Table.from_pylist(rows)

    metadata = dict(table.schema.metadata or {})

    metadata[
        b"chess_ai_lab.feature_names"
    ] = json.dumps(
        feature_names,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")

    metadata[
        b"chess_ai_lab.feature_count"
    ] = str(feature_count).encode("utf-8")

    metadata[
        b"chess_ai_lab.feature_schema_hash"
    ] = feature_schema_hash.encode("utf-8")

    table = table.replace_schema_metadata(metadata)

    pq.write_table(
        table,
        path,
        compression="zstd",
    )


def _current_metadata() -> tuple[list[str], int, str]:
    """
    現在のParquetDatasetが期待するFeature metadataを取得する。

    実装側と同じ計算方法を使うことで、
    テストデータそのものを手書きの19個のFeature名に依存させない。
    """

    feature_names = (
        ParquetDataset._current_feature_names()
    )

    feature_count = len(feature_names)

    feature_schema_hash = (
        ParquetDataset._current_feature_schema_hash()
    )

    return (
        feature_names,
        feature_count,
        feature_schema_hash,
    )


def test_parquet_dataset_accepts_matching_feature_metadata(
    tmp_path,
):
    feature_names, feature_count, feature_schema_hash = (
        _current_metadata()
    )

    path = tmp_path / "train.parquet"

    _write_dataset(
        path,
        feature_names=feature_names,
        feature_count=feature_count,
        feature_schema_hash=feature_schema_hash,
    )

    batch = next(
        ParquetDataset(path).iter_batches()
    )

    assert batch.feature_matrix is not None
    assert batch.feature_matrix.shape == (
        1,
        feature_count,
    )


def test_parquet_dataset_rejects_feature_count_mismatch(
    tmp_path,
):
    feature_names, feature_count, feature_schema_hash = (
        _current_metadata()
    )

    path = tmp_path / "train.parquet"

    _write_dataset(
        path,
        feature_names=feature_names,
        feature_count=feature_count + 1,
        feature_schema_hash=feature_schema_hash,
    )

    with pytest.raises(
        ValueError,
        match="Feature count mismatch",
    ):
        next(
            ParquetDataset(path).iter_batches()
        )


def test_parquet_dataset_rejects_feature_order_mismatch(
    tmp_path,
):
    feature_names, feature_count, feature_schema_hash = (
        _current_metadata()
    )

    modified_names = feature_names.copy()

    modified_names[0], modified_names[1] = (
        modified_names[1],
        modified_names[0],
    )

    path = tmp_path / "train.parquet"

    _write_dataset(
        path,
        feature_names=modified_names,
        feature_count=feature_count,
        feature_schema_hash=feature_schema_hash,
    )

    with pytest.raises(
        ValueError,
        match="Feature Registry order/name mismatch",
    ):
        next(
            ParquetDataset(path).iter_batches()
        )


def test_parquet_dataset_rejects_schema_hash_mismatch(
    tmp_path,
):
    feature_names, feature_count, _ = (
        _current_metadata()
    )

    path = tmp_path / "train.parquet"

    _write_dataset(
        path,
        feature_names=feature_names,
        feature_count=feature_count,
        feature_schema_hash="invalid-hash",
    )

    with pytest.raises(
        ValueError,
        match="Feature schema hash mismatch",
    ):
        next(
            ParquetDataset(path).iter_batches()
        )


def test_parquet_dataset_rejects_missing_feature_metadata(
    tmp_path,
):
    path = tmp_path / "train.parquet"

    table = pa.table(
        {
            "fen": [
                "8/8/8/8/8/8/8/K6k w - - 0 1"
            ],
            "target_cp": [0],
            "source_depth": [20],
            "feature_values": [
                np.zeros(19).tolist()
            ],
        }
    )

    pq.write_table(
        table,
        path,
        compression="zstd",
    )

    with pytest.raises(
        ValueError,
        match="Parquet dataset has no schema metadata",
    ):
        next(
            ParquetDataset(path).iter_batches()
        )
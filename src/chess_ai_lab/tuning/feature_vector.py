from __future__ import annotations

import numpy as np

from chess_ai_lab.evaluation.features import FEATURES
from chess_ai_lab.evaluation.snapshot import EvaluationSnapshot


def snapshot_to_feature_vector(
    snapshot: EvaluationSnapshot,
) -> np.ndarray:
    """
    EvaluationSnapshot を Feature ベクトルへ変換する。

    Feature の順序は FEATURES に従う。
    """

    return np.array(
        [
            snapshot.raw_features.get(name, 0.0)
            for name, _ in FEATURES
        ],
        dtype=np.float64,
    )


def feature_vector_to_raw_features(
    feature_vector: np.ndarray,
) -> dict[str, float]:
    """
    Feature ベクトルを Feature 辞書へ戻す。

    Feature の順序は FEATURES に従う。
    """

    if len(feature_vector) != len(FEATURES):
        raise ValueError(
            f"Expected {len(FEATURES)} features, "
            f"got {len(feature_vector)}."
        )

    return {
        name: float(value)
        for (name, _), value in zip(
            FEATURES,
            feature_vector,
        )
    }
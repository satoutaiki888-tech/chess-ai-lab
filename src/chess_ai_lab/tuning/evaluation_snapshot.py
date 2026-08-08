from dataclasses import dataclass, field

import numpy as np


@dataclass(slots=True)
class EvaluationSnapshot:
    """
    評価関数の計算結果。
    """

    total: float

    feature_vector: np.ndarray

    raw_features: dict[str, float] | None = field(
        default=None,
        kw_only=True,
    )
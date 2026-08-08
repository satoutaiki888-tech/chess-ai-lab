from __future__ import annotations

import numpy as np

from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.tuning.weight_vector import (
    WeightVector,
)

class SGDOptimizer:
    """
    全Weightを同時更新するSGD Optimizer。
    """

    def __init__(
        self,
        learning_rate: float = 0.01,
    ):
        self.learning_rate = learning_rate

    def step(
        self,
        weight_vector: WeightVector,
        gradients: np.ndarray,
    ) -> None:
        """
        Weightを1ステップ更新する。
        """

        weight_vector.apply_gradient(
            gradients,
            self.learning_rate,
        )
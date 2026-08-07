from __future__ import annotations

import numpy as np

from chess_ai_lab.evaluation.weight_manager import WeightManager


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
        weight_manager: WeightManager,
        gradients: np.ndarray,
    ) -> None:
        """
        Weightを1ステップ更新する。
        """

        weights = weight_manager.to_array()

        weights -= (
            self.learning_rate
            * gradients
        )

        weight_manager.from_array(weights)
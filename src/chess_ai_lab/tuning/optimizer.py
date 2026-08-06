from __future__ import annotations

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
        gradients: dict[str, float],
    ) -> None:
        """
        Weightを1ステップ更新する。
        """

        for name, gradient in gradients.items():

            old = weight_manager.get(name)

            new = old - self.learning_rate * gradient

            weight_manager.set(name, new)
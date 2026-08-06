from __future__ import annotations

from abc import ABC, abstractmethod

from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.evolution.evolution import EvolutionResult


class EvolutionStrategy(ABC):
    """
    Evolutionアルゴリズムのインターフェース。
    """

    @abstractmethod
    def evolve_once(
        self,
        parent: WeightManager,
        *,
        games: int = 10,
        depth: int = 2,
        mutation_amount: float = 0.10,
    ) -> EvolutionResult:
        """
        1世代だけ進化を実行する。
        """
        raise NotImplementedError
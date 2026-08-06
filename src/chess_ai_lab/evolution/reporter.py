from __future__ import annotations

from abc import ABC, abstractmethod

from chess_ai_lab.evolution.evolution import EvolutionResult


class EvolutionReporter(ABC):
    """
    Evolution結果の出力インターフェース。
    """

    @abstractmethod
    def report(
        self,
        generation: int,
        result: EvolutionResult,
    ) -> None:
        """
        Evolution結果を出力する。
        """
        raise NotImplementedError
from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.evolution.evolution import EvolutionResult
from chess_ai_lab.evolution.strategy import EvolutionStrategy


class TournamentStrategy(EvolutionStrategy):
    """
    Tournament方式のEvolution。

    未実装。
    """

    def evolve_once(
        self,
        parent: WeightManager,
        *,
        games: int = 10,
        depth: int = 2,
        mutation_amount: float = 0.10,
    ) -> EvolutionResult:
        raise NotImplementedError(
            "TournamentStrategy is not implemented yet."
        )
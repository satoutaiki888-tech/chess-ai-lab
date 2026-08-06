from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.evolution.evolution import EvolutionResult
from chess_ai_lab.evolution.match import play_match
from chess_ai_lab.evolution.selection import select_winner
from chess_ai_lab.evolution.strategy import EvolutionStrategy


class SimpleEvolutionStrategy(EvolutionStrategy):
    """
    現在の mutate → match → selection を実装した Strategy。
    """

    def evolve_once(
        self,
        parent: WeightManager,
        *,
        games: int = 10,
        depth: int = 2,
        mutation_amount: float = 0.10,
        mutation_ratio: float = 0.20,
    ) -> EvolutionResult:

        child, changes = parent.mutate(
            amount=mutation_amount,
            ratio=mutation_ratio,
        )

        match = play_match(
            parent,
            child,
            games=games,
            depth=depth,
        )

        winner = select_winner(
            parent,
            child,
            match,
        )

        adopted = winner is child

        return EvolutionResult(
            winner=winner,
            match=match,
            adopted=adopted,
            changes=changes,
        )
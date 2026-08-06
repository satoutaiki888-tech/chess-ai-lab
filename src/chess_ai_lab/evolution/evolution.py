from dataclasses import dataclass

from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.evolution.match import MatchResult, play_match


@dataclass(slots=True)
class EvolutionResult:
    winner: WeightManager
    match: MatchResult
    adopted: bool
    changes: list[tuple[str, float, float]]


def evolve_once(
    parent: WeightManager,
    *,
    games: int = 10,
    depth: int = 2,
) -> EvolutionResult:
    """
    1世代だけ進化させる。

    Parent
        ↓
    Mutate
        ↓
    Match
        ↓
    Better Weight
    """

    child, changes = parent.mutate()

    match = play_match(
        parent,
        child,
        games=games,
        depth=depth,
    )

    adopted = match.black_wins > match.white_wins

    winner = child if adopted else parent

    return EvolutionResult(
        winner=winner,
        match=match,
        adopted=adopted,
        changes=changes,
    )
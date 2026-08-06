from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.evolution.match import MatchResult


def select_winner(
    parent: WeightManager,
    child: WeightManager,
    result: MatchResult,
) -> WeightManager:
    """
    MatchResultから次世代として採用するWeightを決定する。

    現在のルール
    ----------
    child_wins > parent_wins
        -> child を採用

    それ以外（同点含む）
        -> parent を維持
    """

    if result.child_wins > result.parent_wins:
        return child

    return parent
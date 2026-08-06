from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.evolution.match import MatchResult
from chess_ai_lab.evolution.selection import select_winner


def test_select_parent_when_parent_wins():
    parent = WeightManager()
    child = WeightManager()

    result = MatchResult(
        parent_wins=5,
        child_wins=3,
        draws=2,
    )

    winner = select_winner(
        parent,
        child,
        result,
    )

    assert winner is parent


def test_select_child_when_child_wins():
    parent = WeightManager()
    child = WeightManager()

    result = MatchResult(
        parent_wins=3,
        child_wins=5,
        draws=2,
    )

    winner = select_winner(
        parent,
        child,
        result,
    )

    assert winner is child


def test_select_parent_when_draw():
    parent = WeightManager()
    child = WeightManager()

    result = MatchResult(
        parent_wins=4,
        child_wins=4,
        draws=2,
    )

    winner = select_winner(
        parent,
        child,
        result,
    )

    assert winner is parent
from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.evolution.evolution import evolve, evolve_once
from chess_ai_lab.evolution.match import MatchResult


def test_evolve_once_keeps_parent(monkeypatch):
    parent = WeightManager()

    child, changes = parent.mutate()

    monkeypatch.setattr(
        "chess_ai_lab.evolution.evolution.WeightManager.mutate",
        lambda self: (child, changes),
    )

    monkeypatch.setattr(
        "chess_ai_lab.evolution.evolution.play_match",
        lambda *args, **kwargs: MatchResult(
            parent_wins=5,
            child_wins=3,
            draws=2,
        ),
    )

    result = evolve_once(parent)

    assert result.winner is parent
    assert result.adopted is False
    assert result.match.parent_wins == 5
    assert result.match.child_wins == 3
    assert result.changes == changes


def test_evolve_once_adopts_child(monkeypatch):
    parent = WeightManager()

    child, changes = parent.mutate()

    monkeypatch.setattr(
        "chess_ai_lab.evolution.evolution.WeightManager.mutate",
        lambda self: (child, changes),
    )

    monkeypatch.setattr(
        "chess_ai_lab.evolution.evolution.play_match",
        lambda *args, **kwargs: MatchResult(
            parent_wins=2,
            child_wins=6,
            draws=2,
        ),
    )

    result = evolve_once(parent)

    assert result.winner is child
    assert result.adopted is True
    assert result.match.child_wins == 6
    assert result.changes == changes
    
def test_evolve_zero_generation():
    parent = WeightManager()

    winner = evolve(
        parent,
        generations=0,
    )

    assert winner is parent
    
def test_evolve_calls_evolve_once(monkeypatch):
    parent = WeightManager()

    called = 0

    def fake_evolve_once(parent, *, games, depth):
        nonlocal called

        called += 1

        from chess_ai_lab.evolution.evolution import EvolutionResult
        from chess_ai_lab.evolution.match import MatchResult

        return EvolutionResult(
            winner=parent,
            match=MatchResult(),
            adopted=False,
            changes=[],
        )

    monkeypatch.setattr(
        "chess_ai_lab.evolution.evolution.evolve_once",
        fake_evolve_once,
    )

    evolve(
        parent,
        generations=5,
    )

    assert called == 5        
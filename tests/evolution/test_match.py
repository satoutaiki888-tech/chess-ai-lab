from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.evolution.match import MatchResult, play_match


def test_match_result_defaults():
    result = MatchResult()

    assert result.parent_wins == 0
    assert result.child_wins == 0
    assert result.draws == 0


def test_play_match_zero_games():
    parent = WeightManager()
    child = WeightManager()

    result = play_match(
        parent,
        child,
        games=0,
    )

    assert result.parent_wins == 0
    assert result.child_wins == 0
    assert result.draws == 0


def test_play_match_parent_always_wins(monkeypatch):
    parent = WeightManager()
    child = WeightManager()

    def fake_play_game(white, black):
        return ("1-0", 1)

    monkeypatch.setattr(
        "chess_ai_lab.evolution.match.play_game",
        fake_play_game,
    )

    result = play_match(
        parent,
        child,
        games=1,
    )

    assert result.parent_wins == 1
    assert result.child_wins == 0
    assert result.draws == 0


def test_play_match_parent_wins_when_black(monkeypatch):
    parent = WeightManager()
    child = WeightManager()

    results = iter(
        [
            ("1-0", 1),  # 親=白
            ("0-1", 1),  # 親=黒
        ]
    )

    def fake_play_game(white, black):
        return next(results)

    monkeypatch.setattr(
        "chess_ai_lab.evolution.match.play_game",
        fake_play_game,
    )

    result = play_match(
        parent,
        child,
        games=2,
    )

    assert result.parent_wins == 2
    assert result.child_wins == 0
    assert result.draws == 0


def test_play_match_child_always_wins(monkeypatch):
    parent = WeightManager()
    child = WeightManager()

    results = iter(
        [
            ("0-1", 1),  # 親=白なので子勝ち
            ("1-0", 1),  # 親=黒なので子勝ち
        ]
    )

    def fake_play_game(white, black):
        return next(results)

    monkeypatch.setattr(
        "chess_ai_lab.evolution.match.play_game",
        fake_play_game,
    )

    result = play_match(
        parent,
        child,
        games=2,
    )

    assert result.parent_wins == 0
    assert result.child_wins == 2
    assert result.draws == 0


def test_play_match_draws(monkeypatch):
    parent = WeightManager()
    child = WeightManager()

    def fake_play_game(white, black):
        return ("1/2-1/2", 1)

    monkeypatch.setattr(
        "chess_ai_lab.evolution.match.play_game",
        fake_play_game,
    )

    result = play_match(
        parent,
        child,
        games=3,
    )

    assert result.parent_wins == 0
    assert result.child_wins == 0
    assert result.draws == 3
import chess

from chess_ai_lab.evaluation.features import space


def test_initial_position():
    board = chess.Board()

    assert space.evaluate_space(board) == 0


def test_white_controls_enemy_half():
    board = chess.Board(
        "4k3/8/8/8/3Q4/8/8/4K3 w - - 0 1"
    )

    assert space.evaluate_space(board) > 0


def test_black_controls_enemy_half():
    board = chess.Board(
        "4k3/8/8/3q4/8/8/8/4K3 w - - 0 1"
    )

    assert space.evaluate_space(board) < 0


def test_equal_space():
    board = chess.Board(
        "3qk3/8/8/8/8/8/8/3QK3 w - - 0 1"
    )

    assert space.evaluate_space(board) == 0
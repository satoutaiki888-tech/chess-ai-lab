import chess

from chess_ai_lab.evaluation.features import queen_mobility


def test_initial_position():
    board = chess.Board()

    assert queen_mobility.evaluate_queen_mobility(board) == 0


def test_white_queen_more_mobile():
    board = chess.Board(
        "4k3/8/8/8/3Q4/8/8/4K3 w - - 0 1"
    )

    assert queen_mobility.evaluate_queen_mobility(board) > 0


def test_black_queen_more_mobile():
    board = chess.Board(
        "4k3/8/8/8/8/8/3q4/4K3 w - - 0 1"
    )

    assert queen_mobility.evaluate_queen_mobility(board) < 0
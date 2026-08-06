import chess

from chess_ai_lab.evaluation.features import knight_mobility


def test_initial_position():
    board = chess.Board()

    assert knight_mobility.evaluate_knight_mobility(board) == 0


def test_white_knight_more_mobile():
    board = chess.Board(
        "4k3/8/8/8/3N4/8/8/4K3 w - - 0 1"
    )

    assert knight_mobility.evaluate_knight_mobility(board) > 0


def test_black_knight_more_mobile():
    board = chess.Board(
        "4k3/8/8/8/8/8/3n4/4K3 w - - 0 1"
    )

    assert knight_mobility.evaluate_knight_mobility(board) < 0
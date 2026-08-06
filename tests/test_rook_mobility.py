import chess

from chess_ai_lab.evaluation.features import rook_mobility


def test_initial_position():
    board = chess.Board()

    assert rook_mobility.evaluate_rook_mobility(board) == 0


def test_white_rook_more_mobile():
    board = chess.Board(
        "4k3/8/8/8/4R3/8/8/4K3 w - - 0 1"
    )

    assert rook_mobility.evaluate_rook_mobility(board) > 0


def test_black_rook_more_mobile():
    board = chess.Board(
        "4k3/8/8/8/8/8/4r3/4K3 w - - 0 1"
    )

    assert rook_mobility.evaluate_rook_mobility(board) < 0
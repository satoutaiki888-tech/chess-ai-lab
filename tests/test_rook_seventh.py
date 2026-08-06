import chess

from chess_ai_lab.evaluation.features import rook_seventh


def test_initial_position():
    board = chess.Board()

    assert rook_seventh.evaluate_rook_seventh(board) == 0


def test_white_rook_on_seventh():
    board = chess.Board(
        "4k3/R7/8/8/8/8/8/4K3 w - - 0 1"
    )

    assert rook_seventh.evaluate_rook_seventh(board) == 20


def test_black_rook_on_seventh():
    board = chess.Board(
        "4k3/8/8/8/8/8/r7/4K3 w - - 0 1"
    )

    assert rook_seventh.evaluate_rook_seventh(board) == -20


def test_both_rooks_on_seventh():
    board = chess.Board(
        "4k3/R7/8/8/8/8/r7/4K3 w - - 0 1"
    )

    assert rook_seventh.evaluate_rook_seventh(board) == 0


def test_two_white_rooks_on_seventh():
    board = chess.Board(
        "4k3/R5R1/8/8/8/8/8/4K3 w - - 0 1"
    )

    assert rook_seventh.evaluate_rook_seventh(board) == 40
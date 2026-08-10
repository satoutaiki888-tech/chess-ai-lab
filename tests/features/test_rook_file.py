import chess

from chess_ai_lab.evaluation.features import rook_file


def test_initial_position():
    board = chess.Board()

    assert rook_file.evaluate_rook_file(board) == 0


def test_white_open_file():
    board = chess.Board(
        "4k3/8/8/8/8/8/8/R3K3 w - - 0 1"
    )

    assert rook_file.evaluate_open_file(board) == 20


def test_black_open_file():
    board = chess.Board(
        "r3k3/8/8/8/8/8/8/4K3 w - - 0 1"
    )

    assert rook_file.evaluate_open_file(board) == -20


def test_both_open_file():
    board = chess.Board(
        "r3k3/8/8/8/8/8/8/R3K3 w - - 0 1"
    )

    assert rook_file.evaluate_open_file(board) == 0


def test_white_semi_open_file():
    board = chess.Board(
        "4k3/8/8/p7/8/8/8/R3K3 w - - 0 1"
    )

    assert rook_file.evaluate_semi_open_file(board) == 10


def test_black_semi_open_file():
    board = chess.Board(
        "r3k3/8/8/8/P7/8/8/4K3 w - - 0 1"
    )

    assert rook_file.evaluate_semi_open_file(board) == -10


def test_both_semi_open_file():
    board = chess.Board(
        "r3k3/8/8/P7/p7/8/8/R3K3 w - - 0 1"
    )

    assert rook_file.evaluate_semi_open_file(board) == 0


def test_file_with_both_pawns_is_not_open_or_semi_open():
    board = chess.Board(
        "4k3/8/8/p7/8/P7/8/R3K3 w - - 0 1"
    )

    assert rook_file.evaluate_open_file(board) == 0
    assert rook_file.evaluate_semi_open_file(board) == 0


def test_evaluate_rook_file():
    board = chess.Board(
        "4k3/8/8/p7/8/8/8/R3K3 w - - 0 1"
    )

    assert rook_file.evaluate_rook_file(board) == 10
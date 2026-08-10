import chess

from chess_ai_lab.evaluation.features import connected_rooks


def test_initial_position():
    board = chess.Board()

    assert connected_rooks.evaluate_connected_rooks(board) == 0


def test_white_connected_rooks_rank():
    board = chess.Board(
        "4k3/8/8/8/8/8/8/R5RK w - - 0 1"
    )

    assert connected_rooks.evaluate_connected_rooks(board) == 20


def test_black_connected_rooks_rank():
    board = chess.Board(
        "r5rk/8/8/8/8/8/8/4K3 w - - 0 1"
    )

    assert connected_rooks.evaluate_connected_rooks(board) == -20


def test_white_connected_rooks_file():
    board = chess.Board(
        "4k3/8/R7/8/8/8/R7/4K3 w - - 0 1"
    )

    assert connected_rooks.evaluate_connected_rooks(board) == 20


def test_blocked_rooks():
    board = chess.Board(
        "4k3/8/8/8/8/8/RP4RK/4K3 w - - 0 1"
    )

    assert connected_rooks.evaluate_connected_rooks(board) == 0


def test_both_connected():
    board = chess.Board(
        "r5rk/8/8/8/8/8/8/R5RK w - - 0 1"
    )

    assert connected_rooks.evaluate_connected_rooks(board) == 0
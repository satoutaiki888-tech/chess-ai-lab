import chess

from chess_ai_lab.evaluation.features import bishop_mobility


def test_initial_position():
    board = chess.Board()

    assert bishop_mobility.evaluate_bishop_mobility(board) == 0


def test_white_bishop_more_mobile():
    board = chess.Board(
        "4k3/8/8/8/3B4/8/8/4K3 w - - 0 1"
    )

    assert bishop_mobility.evaluate_bishop_mobility(board) > 0


def test_black_bishop_more_mobile():
    board = chess.Board(
        "4k3/8/8/8/8/8/3b4/4K3 w - - 0 1"
    )

    assert bishop_mobility.evaluate_bishop_mobility(board) < 0
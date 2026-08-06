import chess

from chess_ai_lab.evaluation.features import bishop_pair


def test_initial_position():
    board = chess.Board()

    # 両者ともビショップペアを持つため相殺される
    assert bishop_pair.evaluate_bishop_pair(board) == 0


def test_white_bishop_pair():
    board = chess.Board("4k3/8/8/8/8/8/8/2B1KB2 w - - 0 1")

    assert bishop_pair.evaluate_bishop_pair(board) == 30


def test_black_bishop_pair():
    board = chess.Board("2b1kb2/8/8/8/8/8/8/4K3 w - - 0 1")

    assert bishop_pair.evaluate_bishop_pair(board) == -30


def test_both_have_bishop_pair():
    board = chess.Board("2b1kb2/8/8/8/8/8/8/2B1KB2 w - - 0 1")

    assert bishop_pair.evaluate_bishop_pair(board) == 0
import chess

from chess_ai_lab.evaluation.features.king_safety import (
    evaluate_king_safety,
)


def test_white_castled():
    board = chess.Board(
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQ1RK1 w - - 0 1"
    )

    assert evaluate_king_safety(board) > 0


def test_black_castled():
    board = chess.Board(
        "rnbq1rk1/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1"
    )

    assert evaluate_king_safety(board) < 0


def test_neither_castled():
    board = chess.Board()

    assert evaluate_king_safety(board) == 0
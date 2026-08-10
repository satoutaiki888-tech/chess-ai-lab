import chess

from chess_ai_lab.evaluation.features.material import evaluate_material


def test_initial_position_is_zero():
    board = chess.Board()

    assert evaluate_material(board) == 0


def test_white_missing_queen():
    board = chess.Board()

    board.remove_piece_at(chess.D1)

    assert evaluate_material(board) == -900


def test_black_missing_rook():
    board = chess.Board()

    board.remove_piece_at(chess.A8)

    assert evaluate_material(board) == 500


def test_black_missing_bishop_and_knight():
    board = chess.Board()

    board.remove_piece_at(chess.C8)
    board.remove_piece_at(chess.B8)

    assert evaluate_material(board) == 650
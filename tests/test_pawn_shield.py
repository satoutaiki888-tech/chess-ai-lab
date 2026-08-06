import chess

from chess_ai_lab.evaluation.features import pawn_shield


def test_no_castling():
    board = chess.Board()

    assert pawn_shield.evaluate_pawn_shield(board) == 0


def test_white_full_shield():
    board = chess.Board(
        "4k3/8/8/8/8/8/5PPP/6K1 w - - 0 1"
    )

    assert pawn_shield.evaluate_pawn_shield(board) == 30


def test_black_full_shield():
    board = chess.Board(
        "6k1/5ppp/8/8/8/8/8/4K3 w - - 0 1"
    )

    assert pawn_shield.evaluate_pawn_shield(board) == -30


def test_both_full_shield():
    board = chess.Board(
        "6k1/5ppp/8/8/8/8/5PPP/6K1 w - - 0 1"
    )

    assert pawn_shield.evaluate_pawn_shield(board) == 0


def test_white_partial_shield():
    board = chess.Board(
        "4k3/8/8/8/8/8/5P2/6K1 w - - 0 1"
    )

    assert pawn_shield.evaluate_pawn_shield(board) == 10
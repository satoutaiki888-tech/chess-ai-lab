import chess

from chess_ai_lab.evaluation.features import pawn_structure


def test_initial_position():
    board = chess.Board()

    assert pawn_structure.evaluate_pawn_structure(board) == 0


def test_white_isolated_pawn():
    board = chess.Board("8/8/8/8/8/8/P7/8 w - - 0 1")

    assert pawn_structure.evaluate_isolated_pawn(board) < 0


def test_black_isolated_pawn():
    board = chess.Board("8/p7/8/8/8/8/8/8 w - - 0 1")

    assert pawn_structure.evaluate_isolated_pawn(board) > 0

def test_white_doubled_pawn():
    board = chess.Board("8/8/8/P7/P7/8/8/8 w - - 0 1")

    assert pawn_structure.evaluate_doubled_pawn(board) < 0

def test_black_doubled_pawn():
    board = chess.Board("8/8/8/p7/p7/8/8/8 w - - 0 1")

    assert pawn_structure.evaluate_doubled_pawn(board) > 0    
    
def test_white_passed_pawn():
    board = chess.Board("8/8/8/8/3P4/8/8/8 w - - 0 1")

    assert pawn_structure.evaluate_passed_pawn(board) > 0


def test_black_passed_pawn():
    board = chess.Board("8/8/8/3p4/8/8/8/8 w - - 0 1")

    assert pawn_structure.evaluate_passed_pawn(board) < 0


def test_blocked_pawn_is_not_passed():
    board = chess.Board("8/3p4/8/8/3P4/8/8/8 w - - 0 1")

    assert pawn_structure.evaluate_passed_pawn(board) == 0    
import chess

from chess_ai_lab.evaluation.features import knight_outpost


def test_initial_position():
    board = chess.Board()

    assert knight_outpost.evaluate_knight_outpost(board) == 0


def test_white_outpost():
    board = chess.Board(
        "4k3/8/8/3N4/2P5/8/8/4K3 w - - 0 1"
    )

    assert knight_outpost.evaluate_knight_outpost(board) == 20


def test_black_outpost():
    board = chess.Board(
        "4k3/8/8/8/5p2/4n3/8/4K3 w - - 0 1"
    )

    assert knight_outpost.evaluate_knight_outpost(board) == -20


def test_not_supported_by_pawn():
    board = chess.Board(
        "4k3/8/8/3N4/8/8/8/4K3 w - - 0 1"
    )

    assert knight_outpost.evaluate_knight_outpost(board) == 0


def test_attacked_by_enemy_pawn():
    board = chess.Board(
        "4k3/8/2p5/3N4/2P5/8/8/4K3 w - - 0 1"
    )

    assert knight_outpost.evaluate_knight_outpost(board) == 0


def test_enemy_pawn_can_still_chase():
    board = chess.Board(
        "4k3/2p5/8/3N4/2P5/8/8/4K3 w - - 0 1"
    )

    assert knight_outpost.evaluate_knight_outpost(board) == 0


def test_not_in_enemy_half():
    board = chess.Board(
        "4k3/8/8/8/8/2P5/3N4/4K3 w - - 0 1"
    )

    assert knight_outpost.evaluate_knight_outpost(board) == 0


def test_both_have_outpost():
    board = chess.Board(
        "4k3/8/8/3N4/2P2p2/4n3/8/4K3 w - - 0 1"
    )

    assert knight_outpost.evaluate_knight_outpost(board) == 0


def test_two_white_outposts():
    board = chess.Board(
        "4k3/8/8/2N1N3/1P3P2/8/8/4K3 w - - 0 1"
    )

    assert knight_outpost.evaluate_knight_outpost(board) == 40
import chess

from chess_ai_lab.engine.move_ordering import order_moves


def test_capture_moves_first():
    board = chess.Board("4k3/8/8/8/8/8/3q4/3QK3 w - - 0 1")

    moves = list(board.legal_moves)

    ordered = order_moves(board, moves)

    assert ordered[0] == chess.Move.from_uci("e1d2")
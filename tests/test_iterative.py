import chess

from chess_ai_lab.board import ChessBoard
from chess_ai_lab.engine.iterative import IterativeDeepeningPlayer


def test_iterative_returns_legal_move():
    board = ChessBoard()

    player = IterativeDeepeningPlayer(max_depth=2)

    move = player.choose_move(board)

    assert move in board.legal_moves()


def test_iterative_captures_queen():
    board = ChessBoard()

    board.board().set_fen(
        "4k3/8/8/8/8/8/3q4/3QK3 w - - 0 1"
    )

    player = IterativeDeepeningPlayer(max_depth=2)

    move = player.choose_move(board)

    assert move in {
        chess.Move.from_uci("e1d2"),
        chess.Move.from_uci("d1d2"),
    }
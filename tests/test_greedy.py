import chess

from chess_ai_lab.board import ChessBoard
from chess_ai_lab.engine.greedy import GreedyPlayer


def test_choose_move_returns_legal_move():
    board = ChessBoard()
    player = GreedyPlayer()

    move = player.choose_move(board)

    assert move in board.legal_moves()


def test_choose_move_does_not_change_board():
    board = ChessBoard()
    player = GreedyPlayer()

    before = board.fen()

    player.choose_move(board)

    after = board.fen()

    assert before == after

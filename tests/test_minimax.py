from chess_ai_lab.board import ChessBoard
from chess_ai_lab.engine.minimax import MinimaxPlayer


def test_choose_move_returns_legal_move():
    board = ChessBoard()
    player = MinimaxPlayer(depth=2)

    move = player.choose_move(board)

    assert move in board.legal_moves()


def test_choose_move_does_not_change_board():
    board = ChessBoard()
    player = MinimaxPlayer(depth=2)

    before = board.fen()

    player.choose_move(board)

    after = board.fen()

    assert before == after
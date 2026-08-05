from chess_ai_lab.board import ChessBoard
import chess


def test_initial_board():
    board = ChessBoard()

    assert board.is_game_over() is False
    assert board.turn() is chess.WHITE
    assert len(board.legal_moves()) == 20


def test_push_and_pop():
    board = ChessBoard()

    move = chess.Move.from_uci("e2e4")

    board.push(move)

    assert board.turn() is chess.BLACK

    board.pop()

    assert board.turn() is chess.WHITE


def test_reset():
    board = ChessBoard()

    board.push(chess.Move.from_uci("e2e4"))
    board.reset()

    assert board.turn() is chess.WHITE
    assert len(board.legal_moves()) == 20


def test_fen():
    board = ChessBoard()

    assert board.fen().startswith(
        "rnbqkbnr/pppppppp"
    )
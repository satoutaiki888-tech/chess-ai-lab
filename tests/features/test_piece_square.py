import chess

from chess_ai_lab.board import ChessBoard
from chess_ai_lab.evaluation.features.piece_square import evaluate_piece_square


def test_center_knight_scores_higher():

    board = ChessBoard()

    board.board().set_fen(
        "8/8/8/3N4/8/8/8/8 w - - 0 1"
    )

    center_score = evaluate_piece_square(
        board.board()
    )


    board.board().set_fen(
        "8/8/8/8/8/8/8/N7 w - - 0 1"
    )

    edge_score = evaluate_piece_square(
        board.board()
    )


    assert center_score > edge_score
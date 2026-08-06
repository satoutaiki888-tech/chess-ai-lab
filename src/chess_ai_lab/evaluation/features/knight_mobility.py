import chess

from chess_ai_lab.evaluation.features.mobility_utils import (
    count_piece_mobility,
)


def evaluate_knight_mobility(
    board: chess.Board,
) -> int:
    white = count_piece_mobility(
        board,
        chess.KNIGHT,
        chess.WHITE,
    )

    black = count_piece_mobility(
        board,
        chess.KNIGHT,
        chess.BLACK,
    )

    return white - black
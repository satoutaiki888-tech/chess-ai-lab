import chess

from chess_ai_lab.evaluation.features.mobility_utils import (
    count_piece_mobility,
)


def evaluate_rook_mobility(
    board: chess.Board,
) -> int:
    white = count_piece_mobility(
        board,
        chess.ROOK,
        chess.WHITE,
    )

    black = count_piece_mobility(
        board,
        chess.ROOK,
        chess.BLACK,
    )

    return white - black
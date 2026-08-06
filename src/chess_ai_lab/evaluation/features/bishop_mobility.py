import chess

from chess_ai_lab.evaluation.features.mobility_utils import (
    count_piece_mobility,
)


def evaluate_bishop_mobility(
    board: chess.Board,
) -> int:
    """
    Bishop Mobility の評価
    """

    white = count_piece_mobility(
        board,
        chess.BISHOP,
        chess.WHITE,
    )

    black = count_piece_mobility(
        board,
        chess.BISHOP,
        chess.BLACK,
    )

    return white - black
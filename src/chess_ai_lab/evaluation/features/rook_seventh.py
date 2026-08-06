import chess

ROOK_SEVENTH_BONUS = 20


def _count_rooks_on_seventh(
    board: chess.Board,
    color: chess.Color,
) -> int:
    """
    7段目（黒なら2段目）にいるルーク数を返す。
    """

    count = 0

    for square in board.pieces(chess.ROOK, color):
        rank = chess.square_rank(square)

        if color == chess.WHITE:
            if rank == 6:
                count += 1
        else:
            if rank == 1:
                count += 1

    return count


def evaluate_rook_seventh(
    board: chess.Board,
) -> int:
    """
    Rook on Seventh Rank の評価
    """

    white = _count_rooks_on_seventh(
        board,
        chess.WHITE,
    )

    black = _count_rooks_on_seventh(
        board,
        chess.BLACK,
    )

    return (
        white - black
    ) * ROOK_SEVENTH_BONUS
import chess


def count_piece_mobility(
    board: chess.Board,
    piece_type: chess.PieceType,
    color: chess.Color,
) -> int:
    """
    指定した種類の駒が攻撃しているマス数を返す。
    """

    mobility = 0

    for square in board.pieces(
        piece_type,
        color,
    ):
        mobility += len(
            board.attacks(square)
        )

    return mobility
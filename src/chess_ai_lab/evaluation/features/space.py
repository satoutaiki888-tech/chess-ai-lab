import chess

SPACE_BONUS = 2


def _count_space(
    board: chess.Board,
    color: chess.Color,
) -> int:
    """
    敵陣で支配しているマス数
    """

    controlled = set()

    for square, piece in board.piece_map().items():
        if piece.color != color:
            continue

        controlled.update(
            board.attacks(square)
        )

    count = 0

    for square in controlled:
        rank = chess.square_rank(square)

        if color == chess.WHITE:
            if rank >= 4:
                count += 1
        else:
            if rank <= 3:
                count += 1

    return count


def evaluate_space(
    board: chess.Board,
) -> int:
    """
    Space の評価
    """

    white = _count_space(
        board,
        chess.WHITE,
    )

    black = _count_space(
        board,
        chess.BLACK,
    )

    return (
        white - black
    ) * SPACE_BONUS
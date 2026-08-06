import chess

KNIGHT_OUTPOST_BONUS = 20


def _is_supported_by_pawn(
    board: chess.Board,
    square: chess.Square,
    color: chess.Color,
) -> bool:
    """
    自ポーンで守られているか
    """

    rank = chess.square_rank(square)
    file = chess.square_file(square)

    if color == chess.WHITE:
        support_rank = rank - 1
    else:
        support_rank = rank + 1

    if not (0 <= support_rank <= 7):
        return False

    for support_file in (file - 1, file + 1):
        if not (0 <= support_file <= 7):
            continue

        pawn_square = chess.square(
            support_file,
            support_rank,
        )

        piece = board.piece_at(pawn_square)

        if piece == chess.Piece(chess.PAWN, color):
            return True

    return False


def _is_attacked_by_enemy_pawn(
    board: chess.Board,
    square: chess.Square,
    color: chess.Color,
) -> bool:
    """
    現在敵ポーンに攻撃されているか
    """

    enemy = not color

    for pawn in board.pieces(chess.PAWN, enemy):
        if square in board.attacks(pawn):
            return True

    return False


def _can_be_chased_by_enemy_pawn(
    board: chess.Board,
    square: chess.Square,
    color: chess.Color,
) -> bool:
    """
    将来敵ポーンで追い払えるか
    """

    file = chess.square_file(square)
    rank = chess.square_rank(square)

    enemy = not color

    for pawn in board.pieces(chess.PAWN, enemy):
        pawn_file = chess.square_file(pawn)

        if pawn_file not in (file - 1, file + 1):
            continue

        pawn_rank = chess.square_rank(pawn)

        if color == chess.WHITE:
            # 黒ポーンがまだナイトより前にいる
            if pawn_rank > rank:
                return True
        else:
            # 白ポーンがまだナイトより前にいる
            if pawn_rank < rank:
                return True

    return False


def _is_outpost(
    board: chess.Board,
    square: chess.Square,
    color: chess.Color,
) -> bool:
    rank = chess.square_rank(square)

    if color == chess.WHITE:
        if rank < 4:
            return False
    else:
        if rank > 3:
            return False

    if not _is_supported_by_pawn(
        board,
        square,
        color,
    ):
        return False

    if _is_attacked_by_enemy_pawn(
        board,
        square,
        color,
    ):
        return False

    if _can_be_chased_by_enemy_pawn(
        board,
        square,
        color,
    ):
        return False

    return True


def _count_outposts(
    board: chess.Board,
    color: chess.Color,
) -> int:
    count = 0

    for square in board.pieces(
        chess.KNIGHT,
        color,
    ):
        if _is_outpost(
            board,
            square,
            color,
        ):
            count += 1

    return count


def evaluate_knight_outpost(
    board: chess.Board,
) -> int:
    """
    Knight Outpost の評価
    """

    white = _count_outposts(
        board,
        chess.WHITE,
    )

    black = _count_outposts(
        board,
        chess.BLACK,
    )

    return (
        white - black
    ) * KNIGHT_OUTPOST_BONUS
import chess

OPEN_FILE_BONUS = 20
SEMI_OPEN_FILE_BONUS = 10


def _count_open_rooks(
    board: chess.Board,
    color: chess.Color,
) -> int:
    """
    Open File 上のルーク数
    """

    count = 0

    rooks = board.pieces(chess.ROOK, color)

    for square in rooks:
        file = chess.square_file(square)

        has_white_pawn = any(
            chess.square_file(pawn) == file
            for pawn in board.pieces(chess.PAWN, chess.WHITE)
        )

        has_black_pawn = any(
            chess.square_file(pawn) == file
            for pawn in board.pieces(chess.PAWN, chess.BLACK)
        )

        if not has_white_pawn and not has_black_pawn:
            count += 1

    return count


def _count_semi_open_rooks(
    board: chess.Board,
    color: chess.Color,
) -> int:
    """
    Semi Open File 上のルーク数
    """

    count = 0

    own_pawns = board.pieces(chess.PAWN, color)
    enemy_pawns = board.pieces(chess.PAWN, not color)

    rooks = board.pieces(chess.ROOK, color)

    for square in rooks:
        file = chess.square_file(square)

        has_own = any(
            chess.square_file(pawn) == file
            for pawn in own_pawns
        )

        has_enemy = any(
            chess.square_file(pawn) == file
            for pawn in enemy_pawns
        )

        if (not has_own) and has_enemy:
            count += 1

    return count


def evaluate_open_file(board: chess.Board) -> int:
    """
    Open File の評価
    """

    white = _count_open_rooks(board, chess.WHITE)
    black = _count_open_rooks(board, chess.BLACK)

    return (white - black) * OPEN_FILE_BONUS


def evaluate_semi_open_file(board: chess.Board) -> int:
    """
    Semi Open File の評価
    """

    white = _count_semi_open_rooks(board, chess.WHITE)
    black = _count_semi_open_rooks(board, chess.BLACK)

    return (white - black) * SEMI_OPEN_FILE_BONUS


def evaluate_rook_file(board: chess.Board) -> int:
    """
    Rook File の総合評価
    """

    score = 0

    score += evaluate_open_file(board)
    score += evaluate_semi_open_file(board)

    return score
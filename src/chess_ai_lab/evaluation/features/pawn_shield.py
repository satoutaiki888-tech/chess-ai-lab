import chess

PAWN_SHIELD_BONUS = 10


def _count_pawn_shield(
    board: chess.Board,
    color: chess.Color,
) -> int:
    king = board.king(color)

    if king is None:
        return 0

    if color == chess.WHITE:
        if king == chess.G1:
            squares = [chess.F2, chess.G2, chess.H2]
        elif king == chess.C1:
            squares = [chess.A2, chess.B2, chess.C2]
        else:
            return 0

    else:
        if king == chess.G8:
            squares = [chess.F7, chess.G7, chess.H7]
        elif king == chess.C8:
            squares = [chess.A7, chess.B7, chess.C7]
        else:
            return 0

    return sum(
        1
        for square in squares
        if board.piece_at(square)
        == chess.Piece(chess.PAWN, color)
    )


def evaluate_pawn_shield(board: chess.Board) -> int:
    white = _count_pawn_shield(board, chess.WHITE)
    black = _count_pawn_shield(board, chess.BLACK)

    return (
        white - black
    ) * PAWN_SHIELD_BONUS
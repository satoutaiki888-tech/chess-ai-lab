import chess

CASTLED_BONUS = 30


def evaluate_king_safety(board: chess.Board) -> int:
    """
    キャスリング済みならボーナスを与える。

    White 有利なら正
    Black 有利なら負
    """

    score = 0

    white_king = board.king(chess.WHITE)
    if white_king in (chess.G1, chess.C1):
        score += CASTLED_BONUS

    black_king = board.king(chess.BLACK)
    if black_king in (chess.G8, chess.C8):
        score -= CASTLED_BONUS

    return score
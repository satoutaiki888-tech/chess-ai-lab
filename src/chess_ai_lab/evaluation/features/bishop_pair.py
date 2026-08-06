import chess


BISHOP_PAIR_BONUS = 30


def evaluate_bishop_pair(board: chess.Board) -> int:
    """
    Bishop Pair

    White has two bishops:
        +30

    Black has two bishops:
        -30
    """

    score = 0

    white_bishops = len(
        board.pieces(chess.BISHOP, chess.WHITE)
    )

    black_bishops = len(
        board.pieces(chess.BISHOP, chess.BLACK)
    )

    if white_bishops >= 2:
        score += BISHOP_PAIR_BONUS

    if black_bishops >= 2:
        score -= BISHOP_PAIR_BONUS

    return score
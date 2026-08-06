import chess
from chess_ai_lab.evaluation.weights import PASSED_PAWN_BONUS

ISOLATED_PAWN_PENALTY = 15
DOUBLED_PAWN_PENALTY = 10


def _count_isolated_pawns(board: chess.Board, color: chess.Color) -> int:
    pawns = board.pieces(chess.PAWN, color)

    count = 0

    for square in pawns:
        file = chess.square_file(square)

        has_neighbor = False

        for neighbor_file in (file - 1, file + 1):
            if 0 <= neighbor_file <= 7:
                for other in pawns:
                    if chess.square_file(other) == neighbor_file:
                        has_neighbor = True
                        break

                if has_neighbor:
                    break

        if not has_neighbor:
            count += 1

    return count


def _count_doubled_pawns(board: chess.Board, color: chess.Color) -> int:
    pawns = board.pieces(chess.PAWN, color)

    penalty = 0

    for file in range(8):
        count = sum(
            1
            for square in pawns
            if chess.square_file(square) == file
        )

        if count >= 2:
            penalty += count - 1

    return penalty

def _is_passed_pawn(
    board: chess.Board,
    square: chess.Square,
    color: chess.Color,
) -> bool:
    """
    Passed Pawn 判定
    """

    file = chess.square_file(square)
    rank = chess.square_rank(square)

    enemy = board.pieces(chess.PAWN, not color)

    files = [f for f in (file - 1, file, file + 1) if 0 <= f <= 7]

    for enemy_square in enemy:
        ef = chess.square_file(enemy_square)
        er = chess.square_rank(enemy_square)

        if ef not in files:
            continue

        if color == chess.WHITE:
            if er > rank:
                return False
        else:
            if er < rank:
                return False

    return True


def evaluate_isolated_pawn(board: chess.Board) -> int:
    """
    Isolated Pawn の評価
    """

    white = _count_isolated_pawns(board, chess.WHITE)
    black = _count_isolated_pawns(board, chess.BLACK)

    return (black - white) * ISOLATED_PAWN_PENALTY


def evaluate_doubled_pawn(board: chess.Board) -> int:
    """
    Doubled Pawn の評価
    """

    white = _count_doubled_pawns(board, chess.WHITE)
    black = _count_doubled_pawns(board, chess.BLACK)

    return (black - white) * DOUBLED_PAWN_PENALTY

def evaluate_passed_pawn(board: chess.Board) -> int:
    """
    Passed Pawn の評価
    """

    score = 0

    for square in board.pieces(chess.PAWN, chess.WHITE):
        if _is_passed_pawn(board, square, chess.WHITE):
            rank = chess.square_rank(square)
            score += PASSED_PAWN_BONUS[rank]

    for square in board.pieces(chess.PAWN, chess.BLACK):
        if _is_passed_pawn(board, square, chess.BLACK):
            rank = 7 - chess.square_rank(square)
            score -= PASSED_PAWN_BONUS[rank]

    return score


def evaluate_pawn_structure(board: chess.Board) -> int:
    """
    Pawn Structure の総合評価
    """

    score = 0

    score += evaluate_isolated_pawn(board)
    score += evaluate_doubled_pawn(board)
    score += evaluate_passed_pawn(board)

    return score
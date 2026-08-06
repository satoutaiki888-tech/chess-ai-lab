import chess

from chess_ai_lab.evaluation.weights import PIECE_VALUES


def evaluate_material(board: chess.Board) -> int:
    """
    Material の評価値を返す。

    White が有利なら正、
    Black が有利なら負を返す。
    """

    score = 0

    for piece_type, value in PIECE_VALUES.items():
        white_count = len(board.pieces(piece_type, chess.WHITE))
        black_count = len(board.pieces(piece_type, chess.BLACK))

        score += (white_count - black_count) * value

    return score
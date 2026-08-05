import chess


# ナイト用 Piece Square Table
# 中央に近いほど高評価
KNIGHT_TABLE = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   5,   5,   0, -20, -40,
    -30,   5,  10,  15,  15,  10,   5, -30,
    -30,   0,  15,  20,  20,  15,   0, -30,
    -30,   5,  15,  20,  20,  15,   5, -30,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50,
]


def evaluate_piece_square(board):
    """
    駒の位置評価
    """

    score = 0

    for square, piece in board.piece_map().items():

        if piece.piece_type == chess.KNIGHT:

            value = KNIGHT_TABLE[square]

            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value

    return score
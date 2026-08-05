import chess

# Material 計算で使用する駒価値
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}

# 各特徴量に掛ける重み
FEATURE_WEIGHTS = {
    "material": 1.0,
}
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
    "piece_square": 1.0,
    "mobility": 0.1,

    "isolated_pawn": 1.0,
    "doubled_pawn": 1.0,
    "passed_pawn": 1.0,
    "king_safety": 1.0,
    "bishop_pair": 1.0,
    "open_file": 1.0,
    "semi_open_file": 1.0,
    "pawn_shield": 1.0,
    "knight_outpost": 1.0,
    "connected_rooks": 1.0,
    "rook_seventh": 1.0,
    "space": 1.0,
    "bishop_mobility": 0.1,
    "rook_mobility": 0.1,
    "knight_mobility": 0.1,
    "queen_mobility": 0.01,
}

PASSED_PAWN_BONUS = [
    0,    # 1段目（使用しない）
    10,   # 2段目
    20,   # 3段目
    35,   # 4段目
    55,   # 5段目
    80,   # 6段目
    120,  # 7段目
    0,    # 8段目（昇格）
]
import chess

from chess_ai_lab.evaluation.features import material
from chess_ai_lab.evaluation.features.piece_square import evaluate_piece_square
from chess_ai_lab.evaluation.weights import FEATURE_WEIGHTS


class Evaluator:
    """盤面を評価するクラス"""

    def evaluate(self, board: chess.Board) -> float:
        score = 0.0

        score += (
            material.evaluate(board)
            * FEATURE_WEIGHTS["material"]
            
        )
        
        score += (
            evaluate_piece_square(board)
            * FEATURE_WEIGHTS["piece_square"]
        )

        return score
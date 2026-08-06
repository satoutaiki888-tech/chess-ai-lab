import chess

from chess_ai_lab.evaluation.features import FEATURES
from chess_ai_lab.evaluation.result import EvaluationResult
from chess_ai_lab.evaluation.weight_manager import WeightManager


class Evaluator:
    """盤面を評価するクラス"""

    def __init__(
        self,
        weight_manager: WeightManager | None = None,
    ):
        self.weight_manager = weight_manager or WeightManager()

    def evaluate_detail(self, board: chess.Board) -> EvaluationResult:
        result = EvaluationResult()

        for name, feature in FEATURES:
            raw_score = feature(board)
            weight = self.weight_manager.get(name)
            result.add(name, raw_score * weight)

        return result

    def evaluate(self, board: chess.Board) -> float:
        return self.evaluate_detail(board).total
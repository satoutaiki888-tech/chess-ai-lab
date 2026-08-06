from chess_ai_lab.engine.player import Player
from chess_ai_lab.evaluation.evaluator import Evaluator


class SearchPlayer(Player):
    """探索プレイヤーの共通基底クラス"""

    def __init__(
        self,
        evaluator: Evaluator | None = None,
    ):
        self.evaluator = evaluator or Evaluator()
        self.nodes = 0

    def reset_nodes(self):
        self.nodes = 0
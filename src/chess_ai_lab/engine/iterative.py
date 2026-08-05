from chess_ai_lab.board import ChessBoard
from chess_ai_lab.engine.alphabeta import AlphaBetaPlayer
from chess_ai_lab.engine.player import Player


class IterativeDeepeningPlayer(Player):
    """Iterative Deepening探索プレイヤー"""

    def __init__(self, max_depth: int = 3):
        self.max_depth = max_depth

    def choose_move(self, board: ChessBoard):
        best_move = None

        for depth in range(1, self.max_depth + 1):
            player = AlphaBetaPlayer(depth=depth)
            best_move = player.choose_move(board)

        if best_move is None:
            raise ValueError("No legal moves available.")

        return best_move
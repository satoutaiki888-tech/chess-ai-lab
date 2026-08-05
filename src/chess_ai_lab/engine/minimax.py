import math

import chess

from chess_ai_lab.board import ChessBoard
from chess_ai_lab.engine.search import SearchPlayer


class MinimaxPlayer(SearchPlayer):
    """Minimax探索を行うプレイヤー"""

    def __init__(self, depth: int = 2):
        super().__init__()
        self.depth = depth

    def choose_move(self, board: ChessBoard) -> chess.Move:
        legal_moves = board.legal_moves()

        if not legal_moves:
            raise ValueError("No legal moves available.")

        maximizing = board.turn() == chess.WHITE

        best_move = legal_moves[0]
        best_score = -math.inf if maximizing else math.inf

        for move in legal_moves:
            board.push(move)

            score = self._minimax(
                board,
                self.depth - 1,
                maximizing=not maximizing,
            )

            board.pop()

            if maximizing:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move

        return best_move

    def _minimax(
        self,
        board: ChessBoard,
        depth: int,
        maximizing: bool,
    ) -> float:
        if depth == 0 or board.is_game_over():
            return self.evaluator.evaluate(board.board())

        legal_moves = board.legal_moves()

        if maximizing:
            value = -math.inf

            for move in legal_moves:
                board.push(move)
                value = max(
                    value,
                    self._minimax(board, depth - 1, False),
                )
                board.pop()

            return value

        value = math.inf

        for move in legal_moves:
            board.push(move)
            value = min(
                value,
                self._minimax(board, depth - 1, True),
            )
            board.pop()

        return value
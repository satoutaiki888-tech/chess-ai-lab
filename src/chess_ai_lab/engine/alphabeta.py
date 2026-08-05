import math

from chess_ai_lab import board
from chess_ai_lab.board import ChessBoard
from chess_ai_lab.engine.search import SearchPlayer


class AlphaBetaPlayer(SearchPlayer):
    """Alpha-Beta探索プレイヤー"""

    def __init__(self, depth: int = 2):
        super().__init__()
        self.depth = depth

    def choose_move(self, board: ChessBoard):
        legal_moves = board.legal_moves()

        if not legal_moves:
            raise ValueError("No legal moves available.")

        maximizing = board.turn()

        best_move = legal_moves[0]

        if maximizing:
            best_score = -math.inf

            for move in legal_moves:
                board.push(move)

                score = self._alphabeta(
                    board,
                    self.depth - 1,
                    -math.inf,
                    math.inf,
                    False,
                )

                board.pop()

                if score > best_score:
                    best_score = score
                    best_move = move

        else:
            best_score = math.inf

            for move in legal_moves:
                board.push(move)

                score = self._alphabeta(
                    board,
                    self.depth - 1,
                    -math.inf,
                    math.inf,
                    True,
                )

                board.pop()

                if score < best_score:
                    best_score = score
                    best_move = move

        return best_move

    def _alphabeta(
        self,
        board: ChessBoard,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
    ) -> float:

        if depth == 0 or board.is_game_over():
            return self.evaluator.evaluate(board.board())

        if maximizing:
            value = -math.inf

            for move in board.legal_moves():
                board.push(move)

                value = max(
                    value,
                    self._alphabeta(
                        board,
                        depth - 1,
                        alpha,
                        beta,
                        False,
                    ),
                )

                board.pop()

                alpha = max(alpha, value)

                if beta <= alpha:
                    break

            return value

        value = math.inf

        for move in board.legal_moves():
            board.push(move)

            value = min(
                value,
                self._alphabeta(
                    board,
                    depth - 1,
                    alpha,
                    beta,
                    True,
                ),
            )

            board.pop()

            beta = min(beta, value)

            if beta <= alpha:
                break

        return value
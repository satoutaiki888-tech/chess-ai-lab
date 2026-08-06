import math

from chess_ai_lab import board
from chess_ai_lab.board import ChessBoard
from chess_ai_lab.engine.search import SearchPlayer
from chess_ai_lab.engine.move_ordering import order_moves
from chess_ai_lab.engine.transposition import TranspositionTable


class AlphaBetaPlayer(SearchPlayer):
    """Alpha-Beta探索プレイヤー"""

    def __init__(
        self,
        depth: int = 2,
        evaluator=None,
    ):
        super().__init__(evaluator=evaluator)
        self.depth = depth
        self.table = TranspositionTable()

    def choose_move(self, board: ChessBoard):
        
        self.reset_nodes()
        self.table.clear()
        
        legal_moves = order_moves(
            board.board(),
            board.legal_moves(),
        )

        if not legal_moves:
            raise ValueError("No legal moves available.")

        maximizing = board.turn()

        best_move = legal_moves[0]

        if maximizing:
            best_score = -math.inf

            moves = order_moves(
                board.board(),
                board.legal_moves(),
            )

            for move in moves:
                board.push(move)

                score = self._search_root(
                    board,
                    False,
                )

                board.pop()

                if score > best_score:
                    best_score = score
                    best_move = move

        else:
            best_score = math.inf

            moves = order_moves(
                board.board(),
                board.legal_moves(),
            )

            for move in moves:
                board.push(move)

                score = self._search_root(
                    board,
                    True,
                )

                board.pop()

                if score < best_score:
                    best_score = score
                    best_move = move

        return best_move

    def _search_root(
        self,
        board: ChessBoard,
        maximizing: bool,
    ) -> float:
        """ルートノードからAlpha-Beta探索を開始する"""

        return self._alphabeta(
            board,
            self.depth - 1,
            -math.inf,
            math.inf,
            maximizing,
        )
    
    def _alphabeta(
        self,
        board: ChessBoard,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
    ) -> float:
        
        self.nodes += 1

        key = board.fen()

        cached = self.table.get(key)

        if cached is not None:
            return cached


        if depth == 0 or board.is_game_over():

            score = self.evaluator.evaluate(board.board())

            self.table.put(
                key,
                score,
            )

            return score

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
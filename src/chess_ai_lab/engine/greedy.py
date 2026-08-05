import chess

from chess_ai_lab.board import ChessBoard
from chess_ai_lab.engine.search import SearchPlayer


class GreedyPlayer(SearchPlayer):
    """1手先の評価値が最も良い手を選ぶプレイヤー"""

    def __init__(self):
        super().__init__()

    def choose_move(self, board: ChessBoard) -> chess.Move:
        legal_moves = board.legal_moves()

        if not legal_moves:
            raise ValueError("No legal moves available.")

        if board.board().turn == chess.WHITE:
            best_score = float("-inf")
            best_move = legal_moves[0]

            for move in legal_moves:
                board.push(move)
                score = self.evaluator.evaluate(board.board())
                board.pop()

                if score > best_score:
                    best_score = score
                    best_move = move

        else:
            best_score = float("inf")
            best_move = legal_moves[0]

            for move in legal_moves:
                board.push(move)
                score = self.evaluator.evaluate(board.board())
                board.pop()

                if score < best_score:
                    best_score = score
                    best_move = move

        return best_move
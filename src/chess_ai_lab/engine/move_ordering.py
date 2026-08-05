import chess


def order_moves(board: chess.Board, moves: list[chess.Move]) -> list[chess.Move]:
    """合法手を探索しやすい順に並べる"""

    def score(move: chess.Move) -> int:
        if board.is_capture(move):
            return 100
        return 0

    return sorted(
        moves,
        key=score,
        reverse=True,
    )
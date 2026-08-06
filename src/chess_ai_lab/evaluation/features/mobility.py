import chess


def evaluate_mobility(board: chess.Board) -> float:
    """
    Mobility評価

    白の合法手数 - 黒の合法手数
    """

    turn = board.turn

    white_moves = 0
    black_moves = 0

    board.turn = chess.WHITE
    white_moves = board.legal_moves.count()

    board.turn = chess.BLACK
    black_moves = board.legal_moves.count()

    board.turn = turn

    return float(white_moves - black_moves)
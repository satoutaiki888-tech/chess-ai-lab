from chess_ai_lab.benchmark.epd import EPDPosition
from chess_ai_lab.board import ChessBoard
from chess_ai_lab.engine.alphabeta import AlphaBetaPlayer
from chess_ai_lab.evaluation.evaluator import Evaluator


def evaluate(
    position: EPDPosition,
    evaluator: Evaluator,
    *,
    depth: int = 3,
    verbose: bool = False,
) -> tuple[bool, int]:
    """
    EPDの1局面を評価する。

    Returns
    -------
    (correct, nodes)
    """

    board = ChessBoard()

    board.board().set_epd(position.epd)

    player = AlphaBetaPlayer(
        depth=depth,
        evaluator=evaluator,
    )

    move = player.choose_move(board)

    correct = move in position.best_moves

    if verbose:
        print(position.position_id)
        print("Engine :", move.uci())
        print(
            "Best   :",
            ", ".join(
                m.uci() for m in position.best_moves
            ),
        )
        print("Correct:", correct)
        print()

    return correct, player.nodes
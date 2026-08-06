from dataclasses import dataclass

from chess_ai_lab.board import ChessBoard
from chess_ai_lab.engine.alphabeta import AlphaBetaPlayer
from chess_ai_lab.evaluation.evaluator import Evaluator
from chess_ai_lab.evaluation.weight_manager import WeightManager


@dataclass(slots=True)
class MatchResult:
    parent_wins: int = 0
    child_wins: int = 0
    draws: int = 0


def play_game(
    white: AlphaBetaPlayer,
    black: AlphaBetaPlayer,
) -> tuple[str, int]:
    """
    1局対局する。

    Returns
    -------
    (result, fullmove_number)
    """

    board = ChessBoard()

    while not board.is_game_over():
        if board.turn():
            move = white.choose_move(board)
        else:
            move = black.choose_move(board)

        board.push(move)

    return (
        board.board().result(),
        board.board().fullmove_number,
    )


def play_match(
    white_weights: WeightManager,
    black_weights: WeightManager,
    *,
    games: int = 10,
    depth: int = 2,
) -> MatchResult:
    """
    2つのWeightManagerを指定して複数局対局する。
    """

    white = AlphaBetaPlayer(
        depth=depth,
        evaluator=Evaluator(white_weights),
    )

    black = AlphaBetaPlayer(
        depth=depth,
        evaluator=Evaluator(black_weights),
    )

    result = MatchResult()

    for _ in range(games):
        game_result, _ = play_game(
            white,
            black,
        )

        if game_result == "1-0":
            result.white_wins += 1
        elif game_result == "0-1":
            result.black_wins += 1
        else:
            result.draws += 1

    return result
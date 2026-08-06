import chess
import time
from chess_ai_lab.board import ChessBoard
from chess_ai_lab.benchmark.epd import load_epd
from chess_ai_lab.engine.alphabeta import AlphaBetaPlayer
from chess_ai_lab.evaluation.evaluator import Evaluator
from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.benchmark.result import BenchmarkResult
from chess_ai_lab.benchmark.evaluator import evaluate
from chess_ai_lab.benchmark.runner import run_benchmark

def evaluate(
    position,
    evaluator: Evaluator,
    depth: int = 3,
    verbose: bool = False,
) -> tuple[bool, int]:

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
            ", ".join(m.uci() for m in position.best_moves),
        )

        print("Correct:", correct)

        print()

    return correct, player.nodes


def main() -> None:

    result = run_benchmark(
        WeightManager(),
        depth=3,
    )

    print("=" * 40)
    print("WAC Benchmark")
    print()

    print(f"Positions : {result.positions}")
    print(f"Solved    : {result.solved}")
    print(f"Accuracy  : {result.accuracy * 100:.1f}%")
    print(f"Time      : {result.elapsed:.2f} sec")
    print(f"Nodes     : {result.total_nodes:,}")
    print(f"NPS       : {result.nps:,}")


if __name__ == "__main__":
    main()
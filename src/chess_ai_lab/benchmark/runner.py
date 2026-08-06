import time

from chess_ai_lab.benchmark.epd import load_epd
from chess_ai_lab.benchmark.result import BenchmarkResult
from chess_ai_lab.evaluation.evaluator import Evaluator
from chess_ai_lab.evaluation.weight_manager import WeightManager

from chess_ai_lab.benchmark.evaluator import evaluate


def run_benchmark(
    weights: WeightManager,
    *,
    depth: int = 3,
    epd_path: str = "data/wac.epd",
    limit: int | None = None,
) -> BenchmarkResult:
    """
    EPDベンチマークを実行する。

    Parameters
    ----------
    weights
        使用するWeight。

    depth
        探索深さ。

    epd_path
        EPDファイル。
    """

    evaluator = Evaluator(weights)

    positions = load_epd(epd_path)

    if limit is not None:
        positions = positions[:limit]

    correct = 0
    total_nodes = 0

    start = time.perf_counter()

    for position in positions:

        solved, nodes = evaluate(
            position,
            evaluator,
            depth=depth,
            verbose=False,
        )

        if solved:
            correct += 1

        total_nodes += nodes

    elapsed = time.perf_counter() - start

    return BenchmarkResult(
        positions=len(positions),
        solved=correct,
        total_nodes=total_nodes,
        elapsed=elapsed,
    )
if __name__ == "__main__":

    result = run_benchmark(
        WeightManager(),
        depth=2,
        limit=10,
    )

    print(result)
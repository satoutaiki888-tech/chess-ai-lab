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
    progress_interval: int | None = None,
) -> BenchmarkResult:
    """
    EPDベンチマークを実行する。

    ベンチマークは学習用のlossとは独立して、
    実際にAlpha-Beta探索を行ったときの指し手正答率を測定する。
    """

    if depth < 1:
        raise ValueError("depth must be >= 1")

    if limit is not None and limit < 1:
        raise ValueError("limit must be >= 1 or None")

    if progress_interval is not None and progress_interval < 1:
        raise ValueError("progress_interval must be >= 1 or None")

    evaluator = Evaluator(weights)

    positions = load_epd(epd_path)

    if limit is not None:
        positions = positions[:limit]

    total_positions = len(positions)
    correct = 0
    total_nodes = 0

    start = time.perf_counter()

    for index, position in enumerate(positions, start=1):
        solved, nodes = evaluate(
            position,
            evaluator,
            depth=depth,
            verbose=False,
        )

        if solved:
            correct += 1

        total_nodes += nodes

        if (
            progress_interval is not None
            and (
                index % progress_interval == 0
                or index == total_positions
            )
        ):
            elapsed = time.perf_counter() - start
            nps = int(total_nodes / elapsed) if elapsed > 0 else 0
            accuracy = correct / index if index else 0.0

            print(
                f"Benchmark {index:4d}/{total_positions} | "
                f"Accuracy = {accuracy * 100:5.1f}% | "
                f"Nodes = {total_nodes:,} | "
                f"NPS = {nps:,}"
            )

    elapsed = time.perf_counter() - start

    return BenchmarkResult(
        positions=total_positions,
        solved=correct,
        total_nodes=total_nodes,
        elapsed=elapsed,
    )


if __name__ == "__main__":
    result = run_benchmark(
        WeightManager(),
        depth=2,
        limit=10,
        progress_interval=5,
    )

    print(result)

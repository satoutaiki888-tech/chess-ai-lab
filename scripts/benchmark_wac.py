from __future__ import annotations

import argparse
from pathlib import Path

from chess_ai_lab.benchmark.runner import run_benchmark
from chess_ai_lab.evaluation.weight_manager import WeightManager


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a WAC EPD benchmark against evaluation weights."
    )

    parser.add_argument(
        "--weights",
        type=Path,
        default=None,
        help="JSON weight file. Defaults to built-in FEATURE_WEIGHTS.",
    )

    parser.add_argument(
        "--epd",
        type=Path,
        default=Path("data/wac.epd"),
        help="EPD benchmark file.",
    )

    parser.add_argument(
        "--depth",
        type=int,
        default=2,
        help="Alpha-Beta search depth. Default: 2.",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=32,
        help="Number of positions. Use 0 for all positions. Default: 32.",
    )

    parser.add_argument(
        "--progress",
        type=int,
        default=8,
        help="Print progress every N positions. Default: 8.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    weights = WeightManager()

    if args.weights is not None:
        weights.load_json(args.weights)
        print(f"Weights : {args.weights}")
    else:
        print("Weights : built-in FEATURE_WEIGHTS")

    limit = None if args.limit == 0 else args.limit

    print(f"EPD     : {args.epd}")
    print(f"Depth   : {args.depth}")
    print(
        f"Limit   : {'all' if limit is None else limit}"
    )
    print()
    print("===== WAC Benchmark =====")

    result = run_benchmark(
        weights,
        depth=args.depth,
        epd_path=str(args.epd),
        limit=limit,
        progress_interval=args.progress,
    )

    print()
    print("===== Result =====")
    print(f"Positions : {result.positions}")
    print(f"Solved    : {result.solved}")
    print(f"Accuracy  : {result.accuracy * 100:.1f}%")
    print(f"Time      : {result.elapsed:.2f} sec")
    print(f"Nodes     : {result.total_nodes:,}")
    print(f"NPS       : {result.nps:,}")


if __name__ == "__main__":
    main()
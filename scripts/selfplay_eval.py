from pathlib import Path
import argparse

from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.evolution.match import play_match


def load_weights(path: str | Path) -> WeightManager:
    """JSONからWeightManagerを生成する。"""

    weights = WeightManager()
    weights.load_json(path)
    return weights


def main():
    parser = argparse.ArgumentParser(
        description="Compare two evaluation weight files."
    )

    parser.add_argument(
        "parent",
        help="Path to parent weight JSON.",
    )

    parser.add_argument(
        "child",
        help="Path to child weight JSON.",
    )

    parser.add_argument(
        "--games",
        type=int,
        default=10,
        help="Number of games.",
    )

    parser.add_argument(
        "--depth",
        type=int,
        default=2,
        help="Search depth.",
    )

    args = parser.parse_args()

    parent_weights = load_weights(args.parent)
    child_weights = load_weights(args.child)

    result = play_match(
        parent_weights,
        child_weights,
        games=args.games,
        depth=args.depth,
    )

    print("=== Summary ===")
    print(f"Parent wins : {result.parent_wins}")
    print(f"Child wins  : {result.child_wins}")
    print(f"Draws       : {result.draws}")


if __name__ == "__main__":
    main()
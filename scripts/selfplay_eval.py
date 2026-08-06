from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.evolution.match import play_match


def main():
    parent_weights = WeightManager()

    child_weights, changes = parent_weights.mutate()

    print("=== Mutation ===")

    for name, old, new in changes:
        print(f"{name}: {old:.3f} -> {new:.3f}")

    print()

    result = play_match(
        parent_weights,
        child_weights,
        games=10,
        depth=2,
    )

    print("=== Summary ===")
    print(f"White wins : {result.white_wins}")
    print(f"Black wins : {result.black_wins}")
    print(f"Draws      : {result.draws}")


if __name__ == "__main__":
    main()
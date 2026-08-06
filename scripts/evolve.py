from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.evolution.evolution import evolve_once


def main():
    parent = WeightManager()

    result = evolve_once(
        parent,
        games=10,
        depth=2,
    )

    print("=== Mutation ===")

    for name, old, new in result.changes:
        print(f"{name}: {old:.3f} -> {new:.3f}")

    print()

    print("=== Match ===")
    print(f"Parent wins : {result.match.parent_wins}")
    print(f"Child wins  : {result.match.child_wins}")
    print(f"Draws       : {result.match.draws}")

    print()

    print("=== Selection ===")

    if result.adopted:
        print("Child adopted.")
    else:
        print("Parent retained.")


if __name__ == "__main__":
    main()
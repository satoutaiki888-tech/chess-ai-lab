from chess_ai_lab.evolution.evolution import EvolutionResult
from chess_ai_lab.evolution.reporter import EvolutionReporter


class ConsoleReporter(EvolutionReporter):

    def report(
        self,
        generation: int,
        result: EvolutionResult,
    ) -> None:

        print(f"===== Generation {generation} =====")

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
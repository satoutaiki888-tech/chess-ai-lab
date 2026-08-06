from __future__ import annotations

import json
from pathlib import Path
from random import random

from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.evolution.evolution import EvolutionResult, evolve_once

from chess_ai_lab.evolution.simple_strategy import SimpleEvolutionStrategy
from chess_ai_lab.evolution.strategy import EvolutionStrategy

from chess_ai_lab.evolution.config import EvolutionConfig
import random

class EvolutionRunner:
    """
    Evolution を実行する Runner。

    Responsibilities
    ----------------
    - Evolution実行
    - Weight保存
    - Generation管理
    - Evolutionログ

    Must Not
    --------
    - Mutation
    - Match
    - Selection
    """

    def __init__(
        self,
        *,
        strategy: EvolutionStrategy | None = None,
        weight_dir: str | Path = "weights",
        log_dir: str | Path = "logs",
    ) -> None:
        self.strategy = strategy or SimpleEvolutionStrategy()

        self.weight_dir = Path(weight_dir)
        self.log_dir = Path(log_dir)

        self.weight_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)

    def run_generation(
        self,
        parent: WeightManager,
        *,
        games: int = 10,
        depth: int = 2,
        mutation_amount: float = 0.10,
    ) -> EvolutionResult:
        """
        1世代だけ進化を実行する。
        """

        parent = WeightManager()

        return self.strategy.evolve_once(
            parent,
            games=games,
            depth=depth,
            mutation_amount=mutation_amount,
        )

    def print_result(
        self,
        result: EvolutionResult,
    ) -> None:
        """
        Evolution結果を表示する。
        """

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

    def next_generation_path(self) -> Path:
        """
        次のGenerationの保存先を返す。
        """

        generations = sorted(
            self.weight_dir.glob("generation_*.json")
        )

        generation = len(generations)

        return self.weight_dir / f"generation_{generation:04d}.json"

    def save_weight(
        self,
        result: EvolutionResult,
    ) -> int | None:
        """
        採用されたWeightを保存する。
        """

        if not result.adopted:
            print("No new weight adopted. Skip save.")
            return None

        output_path = self.next_generation_path()

        result.winner.save_json(output_path)

        print(f"Saved: {output_path}")

        return int(output_path.stem.split("_")[1])

    def save_log(
        self,
        generation: int,
        result: EvolutionResult,
    ) -> None:
        """
        Evolution結果をJSONログとして保存する。
        """

        output_path = (
            self.log_dir
            / f"generation_{generation:04d}.json"
        )

        data = {
            "generation": generation,
            "adopted": result.adopted,
            "match": {
                "parent_wins": result.match.parent_wins,
                "child_wins": result.match.child_wins,
                "draws": result.match.draws,
            },
            "changes": [
                {
                    "feature": name,
                    "old": old,
                    "new": new,
                }
                for name, old, new in result.changes
            ],
        }

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(data, f, indent=4)

    def run(
        self,
        initial_weight: WeightManager,
        config: EvolutionConfig,
    ) -> None:
        """
        Evolutionを指定世代数だけ実行する。
        """
        if config.random_seed is not None:
            random.seed(config.random_seed)

        parent = initial_weight

        for _ in range(config.generations):

            result = self.run_generation(
                parent,
                games=config.games,
                depth=config.depth,
                mutation_amount=config.mutation_amount,
            )

            self.print_result(result)

            generation = self.save_weight(result)

            if generation is not None:
                self.save_log(
                    generation,
                    result,
                )

            parent = result.winner
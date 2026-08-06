from dataclasses import dataclass


@dataclass(slots=True)
class EvolutionConfig:
    """
    Evolution実行時の設定。
    """

    generations: int = 1
    games: int = 10
    depth: int = 2
    
    random_seed: int | None = None
    mutation_amount: float = 0.10
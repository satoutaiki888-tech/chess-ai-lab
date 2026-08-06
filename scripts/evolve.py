from chess_ai_lab.evolution.config import EvolutionConfig
from chess_ai_lab.evolution.runner import EvolutionRunner
from chess_ai_lab.evaluation.weight_manager import WeightManager
from pathlib import Path 

def load_initial_weight(
    path: str | Path | None = None,
) -> WeightManager:
    """
    Evolution開始時のWeightを読み込む。

    Parameters
    ----------
    path
        Noneなら初期Weightを使用する。
        指定した場合はJSONから読み込む。
    """

    weight = WeightManager()

    if path is not None:
        path = Path(path)

        print(f"Loading weight: {path}")

        weight.load_json(path)

    return weight

def find_latest_weight(
    weight_dir: str | Path = "weights",
) -> Path | None:
    """
    weights/ 以下から最新GenerationのWeightを返す。

    Returns
    -------
    Path | None
        Weightが存在しない場合はNone。
    """

    weight_dir = Path(weight_dir)

    if not weight_dir.exists():
        return None

    generations = sorted(
        weight_dir.glob("generation_*.json")
    )

    if not generations:
        return None

    return generations[-1]
def main() -> None:

    runner = EvolutionRunner()

    config = EvolutionConfig(
        generations=1,
        games=10,
        depth=2,
        random_seed=42,
        mutation_amount=0.15,
    )

    #
    # Resumeしたい場合だけ
    # ここを書き換える
    #
    resume_latest = True

    if resume_latest:
        resume_path = find_latest_weight()
    else:
        resume_path = None

    initial_weight = load_initial_weight(
        resume_path,
    )

    runner.run(
        initial_weight=initial_weight,
        config=config,
    )


if __name__ == "__main__":
    main()
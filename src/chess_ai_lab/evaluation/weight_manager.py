from chess_ai_lab.evaluation.weights import FEATURE_WEIGHTS
from chess_ai_lab.evaluation.features import FEATURES
import json
from pathlib import Path
import random
import numpy as np

class WeightManager:
    """
    評価関数の重みを管理するクラス。

    現在は FEATURE_WEIGHTS を返すだけだが、
    将来的には JSON 読み込みや学習済み重みを扱う。
    """

    def __init__(self):
        self._weights = FEATURE_WEIGHTS.copy()

    def get(self, name: str) -> float:
        return self._weights[name]

    def set(self, name: str, value: float) -> None:
        self._weights[name] = value

    def to_dict(self) -> dict[str, float]:
        return self._weights.copy()
    
    def to_array(self) -> np.ndarray:
        """
        重みを FEATURES の順番で NumPy 配列として返す。
        """
        return np.array(
            [self._weights[name] for name, _ in FEATURES],
            dtype=np.float64,
        )
        
    def from_array(self, weights: np.ndarray) -> None:
        """
        NumPy 配列から FEATURES の順番で重みを更新する。
        """
        if len(weights) != len(FEATURES):
            raise ValueError(
                f"Expected {len(FEATURES)} weights, got {len(weights)}."
            )

        for (name, _), value in zip(FEATURES, weights):
            self._weights[name] = float(value)    
    
    def save_json(self, path: str | Path) -> None:
        """現在の重みを JSON に保存する。"""
        path = Path(path)
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with path.open("w", encoding="utf-8") as f:
            json.dump(self._weights, f, indent=4)

    def load_json(self, path: str | Path) -> None:
        """JSON から重みを読み込む。"""
        path = Path(path)

        with path.open("r", encoding="utf-8") as f:
            self._weights = json.load(f)
            
    def copy(self) -> "WeightManager":
        """独立した WeightManager を複製する。"""

        copied = WeightManager()
        copied._weights = self._weights.copy()
        return copied        
    def mutate(
        self,
        amount: float = 0.10,
        ratio: float = 0.20,
    ) -> tuple["WeightManager", list[tuple[str, float, float]]]:
        """
        現在の重みから少しだけ変化した次世代を生成する。

        Parameters
        ----------
        amount
            各重みの最大変化量。

        Returns
        -------
        (child, changes)

        child:
            変異後の WeightManager

        changes:
            [(feature_name, old_value, new_value), ...]
        """

        child = self.copy()

        feature_names = list(child._weights.keys())

        mutation_ratio = 0.20

        mutation_count = max(
            1,
            int(len(feature_names) * ratio),
        )

        targets = random.sample(
            feature_names,
            mutation_count,
        )

        changes: list[tuple[str, float, float]] = []

        for name in targets:
            old = child._weights[name]

            delta = random.uniform(-amount, amount)

            new = max(0.0, old + delta)

            child._weights[name] = new

            changes.append((name, old, new))

        return child, changes
    
    def feature_names(self) -> list[str]:
        """
        Feature名を FEATURES の順序で返す。
        """
        return [
            name
            for name, _ in FEATURES
        ]


    def apply_gradient_array(
        self,
        gradients: np.ndarray,
        learning_rate: float,
    ) -> None:
        """
        NumPy配列の勾配をまとめて適用する。

        Parameters
        ----------
        gradients
            FEATURES の順序に対応した勾配

        learning_rate
            学習率
        """

        if len(gradients) != len(FEATURES):
            raise ValueError(
                f"Expected {len(FEATURES)} gradients, "
                f"got {len(gradients)}."
            )

        for (name, _), gradient in zip(
            FEATURES,
            gradients,
        ):
            self._weights[name] -= (
                learning_rate * float(gradient)
            )
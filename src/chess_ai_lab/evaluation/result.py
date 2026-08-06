from dataclasses import dataclass, field


@dataclass
class EvaluationResult:
    """
    評価結果を保持する。

    total:
        評価値の合計。

    details:
        各Featureの評価値。
    """

    total: float = 0.0
    details: dict[str, float] = field(default_factory=dict)

    def add(self, name: str, value: float) -> None:
        """
        Featureを追加する。
        """

        self.details[name] = value
        self.total += value

    def get(self, name: str) -> float:
        """
        Featureの値を取得する。
        """

        return self.details.get(name, 0.0)

    def clear(self) -> None:
        """
        評価結果を初期化する。
        """

        self.total = 0.0
        self.details.clear()
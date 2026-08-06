from dataclasses import dataclass


@dataclass(slots=True)
class BenchmarkResult:
    """
    ベンチマーク結果。

    Attributes
    ----------
    positions
        評価した局面数。

    solved
        正解した局面数。

    total_nodes
        探索した総ノード数。

    elapsed
        ベンチマーク全体の実行時間（秒）。
    """

    positions: int
    solved: int
    total_nodes: int
    elapsed: float

    @property
    def accuracy(self) -> float:
        """
        正答率（0.0〜1.0）
        """
        if self.positions == 0:
            return 0.0

        return self.solved / self.positions

    @property
    def nps(self) -> int:
        """
        Nodes Per Second
        """
        if self.elapsed <= 0:
            return 0

        return int(self.total_nodes / self.elapsed)
    
if __name__ == "__main__":

    result = BenchmarkResult(
        positions=300,
        solved=84,
        total_nodes=1_845_000,
        elapsed=13.5,
    )

    print(result)

    print(result.accuracy)

    print(result.nps)    
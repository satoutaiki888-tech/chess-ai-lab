from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
import time


@dataclass(slots=True)
class BenchmarkTimer:
    """
    学習処理の実行時間を計測する。
    """

    dataset_time: float = 0.0
    evaluation_time: float = 0.0
    gradient_time: float = 0.0
    optimizer_time: float = 0.0

    @contextmanager
    def measure(self, name: str):
        start = time.perf_counter()

        try:
            yield
        finally:
            elapsed = time.perf_counter() - start

            if name == "dataset":
                self.dataset_time += elapsed

            elif name == "evaluation":
                self.evaluation_time += elapsed

            elif name == "gradient":
                self.gradient_time += elapsed

            elif name == "optimizer":
                self.optimizer_time += elapsed

            else:
                raise ValueError(
                    f"Unknown benchmark section: {name}"
                )

    def report(self) -> None:
        total = (
            self.dataset_time
            + self.evaluation_time
            + self.gradient_time
            + self.optimizer_time
        )

        print("\n===== Training Benchmark =====")

        if total == 0:
            print("No benchmark data.")
            return

        print(
            f"Dataset   : {self.dataset_time:.3f}s "
            f"({100 * self.dataset_time / total:.1f}%)"
        )

        print(
            f"Evaluation: {self.evaluation_time:.3f}s "
            f"({100 * self.evaluation_time / total:.1f}%)"
        )

        print(
            f"Gradient  : {self.gradient_time:.3f}s "
            f"({100 * self.gradient_time / total:.1f}%)"
        )

        print(
            f"Optimizer : {self.optimizer_time:.3f}s "
            f"({100 * self.optimizer_time / total:.1f}%)"
        )

        print(
            f"Total     : {total:.3f}s"
        )
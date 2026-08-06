from __future__ import annotations

from collections.abc import Iterable

from chess_ai_lab.evaluation.evaluator import Evaluator
from chess_ai_lab.tuning.loss import texel_loss
from chess_ai_lab.tuning.position import TrainingPosition


class LossEvaluator:
    """
    データセット全体の平均Texel Lossを計算する。
    """

    def __init__(
        self,
        evaluator: Evaluator,
    ):
        self.evaluator = evaluator

    def evaluate(
        self,
        samples: Iterable[TrainingPosition],
        max_samples: int | None = None,
    ) -> float:

        total_loss = 0.0
        sample_count = 0

        for sample in samples:

            if (
                max_samples is not None
                and sample_count >= max_samples
            ):
                break

            score = self.evaluator.evaluate(
                sample.board,
            )

            total_loss += texel_loss(
                score,
                sample.target_cp,
            )

            sample_count += 1

        if sample_count == 0:
            return 0.0

        return total_loss / sample_count
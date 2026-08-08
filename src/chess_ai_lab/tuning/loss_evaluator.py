from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from chess_ai_lab.evaluation.evaluator import Evaluator
from chess_ai_lab.tuning.dataset import ParquetDataset
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

        weights = self.evaluator.weight_manager.to_array()

        # -------------------------
        # Parquet batch path
        # -------------------------

        if isinstance(samples, ParquetDataset):

            total_loss = 0.0
            sample_count = 0

            for batch in samples.iter_batches():

                if (
                    max_samples is not None
                    and sample_count >= max_samples
                ):
                    break

                if batch.feature_matrix is None:
                    raise RuntimeError(
                        "Batch loss evaluation requires "
                        "feature_values."
                    )

                X = batch.feature_matrix
                targets = batch.target_cps

                if max_samples is not None:

                    remaining = (
                        max_samples - sample_count
                    )

                    if len(X) > remaining:
                        X = X[:remaining]
                        targets = targets[:remaining]

                if len(X) == 0:
                    break

                scores = X @ weights

                predicted = 1.0 / (
                    1.0
                    + np.power(
                        10.0,
                        -scores / 400.0,
                    )
                )

                target = 1.0 / (
                    1.0
                    + np.power(
                        10.0,
                        -targets / 400.0,
                    )
                )

                total_loss += float(
                    np.sum(
                        (predicted - target) ** 2
                    )
                )

                sample_count += len(X)

            if sample_count == 0:
                return 0.0

            return total_loss / sample_count

        # -------------------------
        # Legacy path
        # -------------------------

        total_loss = 0.0
        sample_count = 0

        for sample in samples:

            if (
                max_samples is not None
                and sample_count >= max_samples
            ):
                break

            if sample.feature_values is not None:

                score = float(
                    np.dot(
                        sample.feature_values,
                        weights,
                    )
                )

            else:

                if sample.board is None:
                    raise RuntimeError(
                        "TrainingPosition.board is None "
                        "but feature_values are not available."
                    )

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
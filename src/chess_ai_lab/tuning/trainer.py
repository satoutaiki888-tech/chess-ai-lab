from __future__ import annotations

from collections.abc import Iterable

from chess_ai_lab.evaluation.evaluator import Evaluator
from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.tuning.gradient import compute_gradient_array
from chess_ai_lab.tuning.optimizer import SGDOptimizer
from chess_ai_lab.tuning.position import TrainingPosition

from chess_ai_lab.tuning.dataset import ParquetDataset
from chess_ai_lab.tuning.loss_evaluator import LossEvaluator

from pathlib import Path
from chess_ai_lab.tuning.lr_scheduler import ReduceLROnPlateauScheduler

import numpy as np

class Trainer:
    """
    Texel Tuning Trainer
    """

    def __init__(
        self,
        weight_manager: WeightManager,
        learning_rate: float = 0.01,
    ):
        self.weight_manager = weight_manager

        self.evaluator = Evaluator(weight_manager)

        self.optimizer = SGDOptimizer(
            learning_rate=learning_rate,
        )
        
        self.scheduler = ReduceLROnPlateauScheduler(
            optimizer=self.optimizer,
            factor=0.5,
            patience=5,
            min_lr=1e-5,
        )

    def train_epoch(
        self,
        samples: Iterable[TrainingPosition],
        max_samples: int | None = None,
        batch_size: int = 1024,
    ) -> None:
        """
        1エポック学習する。
        """

        gradients = np.zeros(
            len(self.weight_manager.feature_names()),
            dtype=np.float64,
        )

        batch_count = 0
        sample_count = 0

        for sample in samples:

            if (
                max_samples is not None
                and sample_count >= max_samples
            ):
                break

            snapshot = self.evaluator.snapshot(
                sample.board,
            )

            gradients += compute_gradient_array(
                snapshot,
                sample.target_cp,
            )

            batch_count += 1
            sample_count += 1

            if batch_count >= batch_size:

                gradients /= batch_count

                self.optimizer.step(
                    self.weight_manager,
                    gradients,
                )

                gradients.fill(0.0)

                batch_count = 0

        if batch_count > 0:

            gradients /= batch_count

            self.optimizer.step(
                self.weight_manager,
                gradients,
            )
        
    def fit(
        self,
        train_dataset: ParquetDataset,
        valid_dataset: ParquetDataset,
        epochs: int,
        batch_size: int = 1024,
        max_train_samples: int | None = None,
        max_valid_samples: int | None = None,
        best_weight_path: str | Path | None = None,
        patience: int | None = None,
        train_loss_interval: int = 1,
        validation_interval: int = 1,
    ) -> None:
        """
        複数エポック学習する。
        """

        loss_evaluator = LossEvaluator(
            self.evaluator,
        )
        
        best_loss = float("inf")
        
        no_improve_count = 0

        for epoch in range(1, epochs + 1):

            self.train_epoch(
                train_dataset,
                max_samples=max_train_samples,
                batch_size=batch_size,
            )

            train_loss: float | None = None

            if epoch % train_loss_interval == 0:

                train_loss = loss_evaluator.evaluate(
                    train_dataset,
                    max_samples=max_train_samples,
                )

            valid_loss: float | None = None

            if epoch % validation_interval == 0:

                valid_loss = loss_evaluator.evaluate(
                    valid_dataset,
                    max_samples=max_valid_samples,
                )

                self.scheduler.step(valid_loss)
            
            if valid_loss is not None:

                if valid_loss < best_loss:

                    best_loss = valid_loss
                    no_improve_count = 0

                    if best_weight_path is not None:

                        self.weight_manager.save_json(
                            best_weight_path,
                        )

                        print(
                            f"Best weight saved "
                            f"(valid={valid_loss:.6f})"
                        )

                else:

                    no_improve_count += 1

            train_loss_text = (
                f"{train_loss:.6f}"
                if train_loss is not None
                else "-"
            )
            
            valid_loss_text = (
                f"{valid_loss:.6f}"
                if valid_loss is not None
                else "-"
            )            

            print(
                f"Epoch {epoch:3d} | "
                f"LR = {self.optimizer.learning_rate:.6f} | "
                f"Train Loss = {train_loss_text} | "
                f"Valid Loss = {valid_loss_text}"
            )
            if (
                patience is not None
                and no_improve_count >= patience
            ):
                print(
                    f"Early stopping "
                    f"({patience} epochs without improvement)"
                )
                break
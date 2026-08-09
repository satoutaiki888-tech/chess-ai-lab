from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import numpy as np

from chess_ai_lab.evaluation.evaluator import Evaluator
from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.tuning.benchmark import BenchmarkTimer
from chess_ai_lab.tuning.dataset import ParquetDataset
from chess_ai_lab.tuning.evaluation_snapshot import EvaluationSnapshot
from chess_ai_lab.tuning.gradient import (
    compute_gradient_batch,
)
from chess_ai_lab.tuning.loss_evaluator import LossEvaluator
from chess_ai_lab.tuning.lr_scheduler import ReduceLROnPlateauScheduler
from chess_ai_lab.tuning.optimizer import SGDOptimizer
from chess_ai_lab.tuning.position import TrainingPosition
from chess_ai_lab.tuning.weight_vector import WeightVector


class Trainer:
    """
    Texel Tuning Trainer.
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
        X: np.ndarray,
        targets: np.ndarray,
        batch_size: int = 4096,
    ) -> None:

        weight_vector = WeightVector(
            self.weight_manager,
        )

        weights = weight_vector.array

        benchmark = BenchmarkTimer()

        sample_count = len(X)

        for start in range(
            0,
            sample_count,
            batch_size,
        ):

            end = min(
                start + batch_size,
                sample_count,
            )

            X_batch = X[start:end]
            targets_batch = targets[start:end]

            with benchmark.measure("evaluation"):

                totals = X_batch @ weights

            with benchmark.measure("gradient"):

                gradients = compute_gradient_batch(
                    feature_matrix=X_batch,
                    totals=totals,
                    target_cps=targets_batch,
                )

                gradients /= len(X_batch)

            with benchmark.measure("optimizer"):

                self.optimizer.step(
                    weight_vector,
                    gradients,
                )

        weight_vector.sync_to_manager()

        benchmark.report()

        
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

        print("Loading training dataset into memory...")

        train_X, train_targets = self._load_dataset_arrays(
            train_dataset,
            max_samples=max_train_samples,
        )

        print(
            f"Training samples: {len(train_X):,}"
        )

        print("Loading validation dataset into memory...")

        valid_X, valid_targets = self._load_dataset_arrays(
            valid_dataset,
            max_samples=max_valid_samples,
        )

        print(
            f"Validation samples: {len(valid_X):,}"
        )

        loss_evaluator = LossEvaluator(
            self.evaluator,
        )

        best_loss = float("inf")
        no_improve_count = 0

        for epoch in range(1, epochs + 1):

            self.train_epoch(
                train_X,
                train_targets,
                batch_size=batch_size,
            )

            train_loss = None

            if epoch % train_loss_interval == 0:

                train_loss = self._evaluate_arrays(
                    train_X,
                    train_targets,
                    batch_size=batch_size,
                )

            valid_loss = None

            if epoch % validation_interval == 0:

                valid_loss = self._evaluate_arrays(
                    valid_X,
                    valid_targets,
                    batch_size=batch_size,
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
            
    def _load_dataset_arrays(
        self,
        dataset: ParquetDataset,
        max_samples: int | None = None,
    ) -> tuple[np.ndarray, np.ndarray]:

        feature_batches: list[np.ndarray] = []
        target_batches: list[np.ndarray] = []

        collected = 0

        for batch in dataset.iter_batches():

            if batch.feature_matrix is None:
                raise RuntimeError(
                    "Dataset batch does not contain "
                    "feature_matrix."
                )

            X = batch.feature_matrix
            targets = batch.target_cps

            if max_samples is not None:

                remaining = max_samples - collected

                if remaining <= 0:
                    break

                if len(X) > remaining:
                    X = X[:remaining]
                    targets = targets[:remaining]

            feature_batches.append(X)
            target_batches.append(targets)

            collected += len(X)

            if (
                max_samples is not None
                and collected >= max_samples
            ):
                break

        if not feature_batches:
            raise RuntimeError(
                "Dataset contains no training samples."
            )

        X = np.concatenate(
            feature_batches,
            axis=0,
        )

        targets = np.concatenate(
            target_batches,
            axis=0,
        )

        return X, targets        
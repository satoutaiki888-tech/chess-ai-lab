from __future__ import annotations


class ReduceLROnPlateauScheduler:
    """
    Validation Loss が改善しなくなったら
    Learning Rate を減少させる Scheduler。
    """

    def __init__(
        self,
        optimizer,
        factor: float = 0.5,
        patience: int = 5,
        min_lr: float = 1e-5,
    ):
        self.optimizer = optimizer

        self.factor = factor
        self.patience = patience
        self.min_lr = min_lr

        self.best_loss = float("inf")
        self.bad_epochs = 0

    def step(
        self,
        validation_loss: float,
    ) -> None:

        if validation_loss < self.best_loss:

            self.best_loss = validation_loss
            self.bad_epochs = 0
            return

        self.bad_epochs += 1

        if self.bad_epochs < self.patience:
            return

        new_lr = max(
            self.optimizer.learning_rate * self.factor,
            self.min_lr,
        )

        if new_lr < self.optimizer.learning_rate:

            self.optimizer.learning_rate = new_lr

            print(
                f"Learning rate reduced to "
                f"{new_lr:.6f}"
            )

        self.bad_epochs = 0
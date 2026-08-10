from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class TrainingConfig:
    """
    Texel Tuning 実行時の設定。
    """

    learning_rate: float = 0.1

    epochs: int = 100

    batch_size: int = 1024

    max_train_samples: int | None = 1000

    max_valid_samples: int | None = 200

    patience: int | None = 10

    train_loss_interval: int = 1

    validation_interval: int = 1

    best_weight_path: Path = Path(
        "weights/best_weight.json",
    )

    output_weight_path: Path = Path(
        "weights_trained.json",
    )


DEV_CONFIG = TrainingConfig(
    learning_rate=1.0,
    epochs=30,
    batch_size=4096,
    max_train_samples=50_000,
    max_valid_samples=10_000,
    patience=3,
    train_loss_interval=10,
    validation_interval=5,
)


PRODUCTION_CONFIG = TrainingConfig(
    learning_rate=1,
    epochs=100,
    batch_size=4096,
    max_train_samples=None,
    max_valid_samples=10_000,
    patience=10,
    train_loss_interval=10,
    validation_interval=5,
)
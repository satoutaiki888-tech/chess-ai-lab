import argparse

from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.tuning.config import PRODUCTION_CONFIG
from chess_ai_lab.tuning.dataset import ParquetDataset
from chess_ai_lab.tuning.trainer import Trainer

parser = argparse.ArgumentParser()
parser.add_argument(
    "--fresh",
    action="store_true",
    help="Start training from the built-in evaluation weights instead of resuming from best_weight.json.",
)
args = parser.parse_args()

config = PRODUCTION_CONFIG
weights = WeightManager()

best_weight_path = config.best_weight_path

if best_weight_path.exists() and not args.fresh:
    weights.load_json(best_weight_path)
    print(f"Resume training from {best_weight_path}")
elif args.fresh:
    print("Fresh training from built-in evaluation weights")

trainer = Trainer(
    weight_manager=weights,
    learning_rate=config.learning_rate,
)

train_dataset = ParquetDataset(
    "data/training/train.parquet",
)

valid_dataset = ParquetDataset(
    "data/training/valid.parquet",
)

trainer.fit(
    train_dataset=train_dataset,
    valid_dataset=valid_dataset,
    epochs=config.epochs,
    batch_size=config.batch_size,
    max_train_samples=config.max_train_samples,
    max_valid_samples=config.max_valid_samples,
    best_weight_path=best_weight_path,
    patience=config.patience,
    train_loss_interval=config.train_loss_interval,
    validation_interval=config.validation_interval,
)

weights.save_json(
    config.output_weight_path,
)

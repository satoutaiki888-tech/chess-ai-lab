from chess_ai_lab.evaluation import weight_manager
from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.tuning.dataset import ParquetDataset
from chess_ai_lab.tuning.trainer import Trainer

weights = WeightManager()

from pathlib import Path

best_weight_path = Path("weights/best_weight.json")

if best_weight_path.exists():
    weights.load_json(best_weight_path)
    print(f"Resume training from {best_weight_path}")

trainer = Trainer(
    weight_manager=weights,
    learning_rate=0.1,
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
    epochs=100,
    max_train_samples=1000,
    max_valid_samples=200,
    best_weight_path="weights/best_weight.json",
    patience=10,
)

weights.save_json(
    "weights_trained.json",
)
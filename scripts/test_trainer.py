from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.tuning.dataset import ParquetDataset
from chess_ai_lab.tuning.trainer import Trainer

weights = WeightManager()

trainer = Trainer(
    weight_manager=weights,
    learning_rate=0.1,
)

before = weights.to_dict()

dataset = ParquetDataset(
    "data/training/train.parquet",
)

trainer.train_epoch(
    dataset,
    max_samples=100,
)

after = weights.to_dict()

changed = 0

for name in before:

    if before[name] != after[name]:

        changed += 1

        print(
            f"{name}: {before[name]} -> {after[name]}"
        )

print()

print(f"Changed weights: {changed}")
from chess_ai_lab.evaluation.evaluator import Evaluator
from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.tuning.dataset import ParquetDataset
from chess_ai_lab.tuning.loss_evaluator import LossEvaluator

weights = WeightManager()

evaluator = Evaluator(weights)

loss_evaluator = LossEvaluator(evaluator)

dataset = ParquetDataset(
    "data/training/train.parquet",
)

loss = loss_evaluator.evaluate(
    dataset,
    max_samples=100,
)

print(loss)
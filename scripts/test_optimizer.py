from chess_ai_lab.evaluation.weight_manager import WeightManager
from chess_ai_lab.tuning.optimizer import SGDOptimizer

weights = WeightManager()

optimizer = SGDOptimizer(
    learning_rate=0.1,
)

name = next(iter(weights.to_dict()))

before = weights.get(name)

optimizer.step(
    weights,
    {
        name: 2.0,
    },
)

after = weights.get(name)

print(name)
print(before)
print(after)
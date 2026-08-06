from chess_ai_lab.tuning.loss import cp_to_probability
from chess_ai_lab.tuning.loss import texel_loss

print(cp_to_probability(0))
print(cp_to_probability(400))
print(cp_to_probability(-400))

print(texel_loss(100, 100))
print(texel_loss(0, 400))
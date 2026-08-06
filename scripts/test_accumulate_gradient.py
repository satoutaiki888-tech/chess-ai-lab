import chess

from chess_ai_lab.evaluation.evaluator import Evaluator
from chess_ai_lab.tuning.gradient import accumulate_gradients

board = chess.Board(
    "7r/1p3k2/p1bPR3/5p2/2B2P1p/8/PP4P1/3K4 b - -"
)

snapshot = Evaluator().snapshot(board)

gradients = {
    name: 0.0
    for name in snapshot.raw_features
}

accumulate_gradients(
    snapshot=snapshot,
    target_cp=69,
    gradients=gradients,
)

for name, value in gradients.items():
    if value != 0.0:
        print(f"{name}: {value}")
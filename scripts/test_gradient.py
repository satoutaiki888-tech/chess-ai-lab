import chess

from chess_ai_lab.evaluation.evaluator import Evaluator
from chess_ai_lab.tuning.gradient import compute_gradients

board = chess.Board()

snapshot = Evaluator().snapshot(board)

gradients = compute_gradients(
    snapshot=snapshot,
    target_cp=100,
)

for name, value in gradients.items():
    if value != 0:
        print(name, value)
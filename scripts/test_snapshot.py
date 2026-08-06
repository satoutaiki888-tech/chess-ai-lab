import chess

from chess_ai_lab.evaluation.evaluator import Evaluator

board = chess.Board()

snapshot = Evaluator().snapshot(board)

print(snapshot.total)

for name, value in list(snapshot.raw_features.items())[:10]:
    print(name, value)
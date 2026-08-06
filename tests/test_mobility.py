import chess

from chess_ai_lab.evaluation.features.mobility import evaluate_mobility


def test_mobility_returns_difference():

    board = chess.Board()

    score = evaluate_mobility(board)

    assert isinstance(score, float)
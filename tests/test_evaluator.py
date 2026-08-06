import chess

from chess_ai_lab.evaluation.evaluator import Evaluator


def test_evaluate_detail():
    evaluator = Evaluator()

    board = chess.Board()

    result = evaluator.evaluate_detail(board)

    assert "material" in result.details
    assert "piece_square" in result.details
    assert "mobility" in result.details
    assert "passed_pawn" in result.details

    assert isinstance(result.total, float)
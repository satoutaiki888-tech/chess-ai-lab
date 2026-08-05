from chess_ai_lab.evaluation.weights import FEATURE_WEIGHTS


def test_feature_weights_exist():
    assert "material" in FEATURE_WEIGHTS
    assert "piece_square" in FEATURE_WEIGHTS


def test_feature_weights_are_positive():
    for weight in FEATURE_WEIGHTS.values():
        assert weight >= 0
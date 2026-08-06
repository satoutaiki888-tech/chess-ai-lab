from chess_ai_lab.evaluation.result import EvaluationResult


def test_add_feature():
    result = EvaluationResult()

    result.add("material", 100)

    assert result.total == 100
    assert result.get("material") == 100


def test_multiple_features():
    result = EvaluationResult()

    result.add("material", 100)
    result.add("mobility", -5)

    assert result.total == 95
    assert result.get("material") == 100
    assert result.get("mobility") == -5


def test_clear():
    result = EvaluationResult()

    result.add("material", 100)

    result.clear()

    assert result.total == 0
    assert result.details == {}
from chess_ai_lab.evaluation.weight_manager import WeightManager


def test_copy_is_independent():
    parent = WeightManager()

    parent.set("material", 2.0)

    child = parent.copy()

    child.set("material", 3.0)

    assert parent.get("material") == 2.0
    assert child.get("material") == 3.0
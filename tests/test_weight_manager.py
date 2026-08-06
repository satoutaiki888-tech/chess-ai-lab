from chess_ai_lab.evaluation.weight_manager import WeightManager


def test_save_and_load_json(tmp_path):
    wm = WeightManager()

    wm.set("material", 2.5)

    path = tmp_path / "weights.json"

    wm.save_json(path)

    wm2 = WeightManager()
    wm2.load_json(path)

    assert wm2.get("material") == 2.5
from chess_ai_lab.evaluation.weight_manager import WeightManager


def test_mutate_creates_child_with_one_or_two_changes():
    wm = WeightManager()

    before = wm.to_dict()

    child, changes = wm.mutate()

    # 親は変化しない
    assert wm.to_dict() == before

    after = child.to_dict()

    changed = [
        name
        for name in before
        if before[name] != after[name]
    ]

    # 変更数は1〜2個
    assert 1 <= len(changed) <= 2
    assert len(changes) == len(changed)

    # changes の内容が実際の変更と一致する
    for name, old, new in changes:
        assert name in changed
        assert old == before[name]
        assert new == after[name]
        assert old != new
from benchmark.generate import generate_instance


def test_generate_is_deterministic_per_seed():
    a_items, a_cap = generate_instance(20, seed=123)
    b_items, b_cap = generate_instance(20, seed=123)
    assert a_cap == b_cap
    assert [(it.weight, it.value) for it in a_items] == [(it.weight, it.value) for it in b_items]


def test_generate_different_seeds_differ():
    a_items, _ = generate_instance(20, seed=1)
    b_items, _ = generate_instance(20, seed=2)
    assert [(it.weight, it.value) for it in a_items] != [(it.weight, it.value) for it in b_items]


def test_generate_capacity_is_half_total_weight_by_default():
    items, cap = generate_instance(50, seed=0)
    total = sum(it.weight for it in items)
    assert cap == total // 2

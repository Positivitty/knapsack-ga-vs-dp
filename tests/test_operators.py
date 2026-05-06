import numpy as np

from ga.operators import bitflip_mutate, tournament_select, uniform_crossover


def test_tournament_select_picks_higher_fitness_on_average():
    rng = np.random.default_rng(0)
    pop = np.arange(10).reshape(10, 1).astype(np.uint8)
    fits = np.arange(10)
    parents = tournament_select(rng, pop, fits, n_parents=1000, k=3)
    # mean parent index should be well above population mean (4.5)
    assert parents.mean() > 6


def test_uniform_crossover_preserves_shape_and_alleles():
    rng = np.random.default_rng(0)
    parents = np.array([[1, 1, 1, 1], [0, 0, 0, 0]], dtype=np.uint8)
    children = uniform_crossover(rng, parents, p_crossover=1.0)
    assert children.shape == parents.shape
    # every bit must come from one of the parents (i.e. be 0 or 1)
    assert ((children == 0) | (children == 1)).all()
    # paired children together must contain exactly all the alleles of both parents
    assert (children[0] + children[1] == 1).all()


def test_uniform_crossover_no_op_when_p_zero():
    rng = np.random.default_rng(0)
    parents = np.array([[1, 1, 1, 1], [0, 0, 0, 0]], dtype=np.uint8)
    children = uniform_crossover(rng, parents, p_crossover=0.0)
    assert (children == parents).all()


def test_bitflip_mutate_zero_rate_is_identity():
    rng = np.random.default_rng(0)
    pop = np.array([[1, 0, 1, 0]], dtype=np.uint8)
    out = bitflip_mutate(rng, pop, p_mutate=0.0)
    assert (out == pop).all()


def test_bitflip_mutate_full_rate_inverts():
    rng = np.random.default_rng(0)
    pop = np.array([[1, 0, 1, 0]], dtype=np.uint8)
    out = bitflip_mutate(rng, pop, p_mutate=1.0)
    assert (out == np.array([[0, 1, 0, 1]], dtype=np.uint8)).all()

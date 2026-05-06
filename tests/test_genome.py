import numpy as np

from common.item import Item
from ga.genome import decode, fitness, items_to_arrays, random_population


def test_random_population_shape_and_dtype():
    rng = np.random.default_rng(0)
    pop = random_population(rng, pop_size=20, n=10)
    assert pop.shape == (20, 10)
    assert pop.dtype == np.uint8
    assert ((pop == 0) | (pop == 1)).all()


def test_fitness_zero_for_infeasible():
    weights = np.array([5, 5, 5])
    values = np.array([10, 10, 10])
    pop = np.array([[1, 1, 1], [1, 0, 0]], dtype=np.uint8)
    fits = fitness(pop, weights, values, capacity=6)
    assert fits[0] == 0  # weight 15 > 6
    assert fits[1] == 10


def test_fitness_picks_max_when_feasible():
    weights = np.array([1, 2, 3])
    values = np.array([5, 8, 9])
    pop = np.array([[1, 1, 1]], dtype=np.uint8)
    assert fitness(pop, weights, values, capacity=10)[0] == 22


def test_decode_returns_chosen_indices():
    genome = np.array([1, 0, 1, 0, 1], dtype=np.uint8)
    assert decode(genome) == [0, 2, 4]


def test_items_to_arrays_roundtrip():
    items = [Item(1, 2), Item(3, 4), Item(5, 6)]
    w, v = items_to_arrays(items)
    assert list(w) == [1, 3, 5]
    assert list(v) == [2, 4, 6]

import pytest

from gencipher.crossover import ParentsLengthError
from gencipher.utils import select_parent


@pytest.mark.parametrize("crossover_type", [
    "order-one",
    "partially-mapped",
    "cycle",
    "full"
])
def test_crossover_methods(crossover_type, monogram_gencipher):
    for _ in range(60):
        monogram_gencipher.decipher(cipher_text="cryptogram",
                                    crossover_type=crossover_type,
                                    max_iter=0,
                                    n_population=20)
        parent1 = select_parent(monogram_gencipher.population)
        parent2 = select_parent(monogram_gencipher.population)
        offspring = monogram_gencipher.crossover(parent1, parent2)
        assert len(offspring) == len(parent1)
        assert sorted(offspring) == sorted(parent1)


@pytest.mark.parametrize("crossover_type", [
    "order-one",
    "partially-mapped",
    "cycle",
    "full"
])
def test_parents_length_error(crossover_type, monogram_gencipher):
    monogram_gencipher.decipher(cipher_text="",
                                crossover_type=crossover_type,
                                max_iter=0)
    parent1 = "ABC"
    parent2 = "DE"

    with pytest.raises(ParentsLengthError):
        monogram_gencipher.crossover(parent1, parent2)

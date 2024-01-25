import pytest

from gencipher.utils import InvalidInputError, select_parent
from gencipher.ngram import Ngram


def test_fitness_select_parent():
    # Test with a simple population and fitness scores
    population_fitness = {"A": 0.2, "B": 0.3, "C": 0.5}
    selected_parent = select_parent(population_fitness)
    assert selected_parent in population_fitness

    # Test with a population where one individual has a fitness score
    # of 0
    population_fitness = {"A": 0, "B": 0.4, "C": 0.6}
    selected_parent = select_parent(population_fitness)
    assert selected_parent == "B" or selected_parent == "C"

    # Test with a population where all individuals have equal fitness
    population_fitness = {"X": 0.3, "Y": 0.3, "Z": 0.3}
    selected_parent = select_parent(population_fitness)
    assert selected_parent in population_fitness


def test_input_error(monogram_gencipher):
    invalid_input = "invalid_input"

    # Test InvalidInputError in Ngram class
    with pytest.raises(InvalidInputError):
        Ngram(ngram_type=invalid_input, scores_folder="")

    # Test InvalidInputError in Mutation class
    with pytest.raises(InvalidInputError):
        monogram_gencipher.decipher(cipher_text="a",
                                    mutation_type=invalid_input)

    # Test InvalidInputError in Crossover class
    with pytest.raises(InvalidInputError):
        monogram_gencipher.decipher(cipher_text="a",
                                    crossover_type=invalid_input)

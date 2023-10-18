from os.path import join, dirname
from gencipher.fitness import select_parent, Ngram, NgramType


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


def test_fitness_ngram_class():
    parent_folder = join(dirname(__file__), "..")
    scores_folder = join(parent_folder, "data", "ngrams_scores")

    # Test the load of ngram score files
    for ngram_type in NgramType.values():
        ngram = Ngram(ngram_type, scores_folder)

    # Test the compute_fitness method
    text = "HELLO"
    fitness = ngram.compute_fitness(text)
    assert isinstance(fitness, float)
    assert fitness <= 0

    # Test the generate_population method
    cipher_text = "Rovvy, Nre qn yvi tsirk nzro."
    n_population = 10
    population_fitness = ngram.generate_population(cipher_text, n_population)
    assert len(population_fitness) == n_population

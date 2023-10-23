from gencipher.ngram import Ngram, NgramType


def test_fitness_ngram_class():
    # Test the load of ngram score files
    for ngram_type in NgramType.values():
        ngram = Ngram(ngram_type)

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

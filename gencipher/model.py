import pstats
from numpy import inf
from random import random
from cProfile import Profile

from utils import decrypt
from mutation import Mutation
from crossover import Crossover
from fitness import select_parent, generate_population, Ngram


class GeneticDecipher(Crossover, Mutation):
    def __init__(
            self,
            ngram_type : str = "quadgram",
            mutation_type : str = "scramble",
            mutation_rate : float = 0.01,
            crossover_type : str = "order-one",
            crossover_rate : float = 0.6
    ) -> None:
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

        self._set_mutation(mutation_type)
        self._set_crossover(crossover_type)
        self.ngram = Ngram(ngram_type)

    def decipher(
            self,
            cipher_text: str,
            max_iterations : int = 20,
            n_population : int = 100
    ) -> str:
        self.n_population = n_population
        population = generate_population(cipher_text,
                                         self.n_population,
                                         self.ngram)
        self.history = []
        best_key = ("", -inf)

        for idx in range(max_iterations):
            population = self.evolve_population(population)
            best_idx_key = max(population.items(), key=lambda x: x[1])

            if best_idx_key[1] > best_key[1]:
                best_key = best_idx_key
            deciphered_text = decrypt(cipher_text, best_key[0])

            self.history.append((idx, best_key, deciphered_text))

        return deciphered_text

    def evolve_population(self, population: dict) -> dict:
        new_population = {}
        for i in range(self.n_population):
            key1 = select_parent(population)
            key2 = select_parent(population)
            if population[key1] > population[key2]:
                winner, loser = key1, key2
            else:
                winner, loser = key2, key1
            new_key = winner
            new_fitness = population[winner]

            if random() < self.crossover_rate:
                new_key = self.crossover(winner, loser)
                new_fitness = self.ngram.compute_fitness(new_key)
            if random() < self.mutation_rate:
                new_key = self.mutation(new_key)
                new_fitness = self.ngram.compute_fitness(new_key)
            new_population[new_key] = new_fitness

        return new_population


def main():
    with Profile() as pr:
        gencipher = GeneticDecipher(ngram_type="quintgram")
        cipher_text = """
        Zc hdzq tr Zdytzir Gqstzir Zqltgtir, sezzdhgql ea nmq Dlztqr ea nmq
        Helnm, Fqhqldu ea nmq Aquty Uqftehr, dhg uecdu rqlodhn ne nmq nliq
        qzvqlel, Zdlsir Dilqutir. Adnmql ne d zilgqlqg reh, mirvdhg ne d
        zilgqlqg ktaq. Dhg T ktuu mdoq zc oqhfqdhsq, th nmtr utaq el nmq hqyn.
        """

        gencipher.decipher(cipher_text)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()

    # print(deciphered_text)
    # print()
    # print(gencipher.history)


if __name__ == "__main__":
    main()

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
            crossover_type : str = "full",
            crossover_rate : float = 0.6
    ) -> None:
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

        self._set_mutation(mutation_type)
        self._set_crossover(crossover_type)
        self.ngram = Ngram(ngram_type)

    def FX(self, winner: str, loser: str) -> str:
        target_fitness = self.population[winner]
        target_key = list(winner)
        source_key = list(loser)

        for idx in range(len(target_key)):
            if source_key[idx] != target_key[idx]:
                new_key = target_key[:]
                temp_idx = new_key.index(source_key[idx])
                new_key[idx], new_key[temp_idx] = source_key[idx], new_key[idx]

                new_text = decrypt(self.cipher_text, new_key)
                new_fitness = self.ngram.compute_fitness(new_text)
                if new_fitness > target_fitness:
                    target_key = new_key
                    target_fitness = new_fitness

        return "".join(target_key)

    def evolve_population(self, population: dict) -> dict:
        new_population = {}
        for _ in range(self.n_population):
            key1 = select_parent(population)
            key2 = select_parent(population)
            if population[key1] > population[key2]:
                winner, loser = key1, key2
            else:
                winner, loser = key2, key1
            new_key = winner
            new_fitness = fitness_target = population[winner]

            if random() < self.crossover_rate:
                new_key = self.crossover(winner, loser)
                new_text = decrypt(self.cipher_text, new_key)
                new_fitness = self.ngram.compute_fitness(new_text)
                if fitness_target > new_fitness:
                    new_key = winner
                    new_fitness = fitness_target
            if random() < self.mutation_rate:
                new_key = self.mutation(new_key)
                new_text = decrypt(self.cipher_text, new_key)
                new_fitness = self.ngram.compute_fitness(new_text)
            new_population[new_key] = new_fitness

        return new_population

    def decipher(
            self,
            cipher_text: str,
            max_iter: int = 20,
            n_population : int = 100
    ) -> str:
        self.cipher_text = cipher_text
        self.n_population = n_population
        self.population = generate_population(self.cipher_text,
                                              self.n_population,
                                              self.ngram)
        self.history = {"best_key": [],
                        "deciphered_text": []}
        best_key = ("", -inf)

        for idx in range(max_iter):
            self.population = self.evolve_population(self.population)
            best_idx_key = max(self.population.items(), key=lambda x: x[1])

            if best_idx_key[1] > best_key[1]:
                best_key = best_idx_key
            deciphered_text = decrypt(self.cipher_text, best_key[0])

            self.history["best_key"].append(best_key)
            self.history["deciphered_text"].append(deciphered_text)

        return deciphered_text


def main():
    with Profile() as pr:
        gencipher = GeneticDecipher(ngram_type="quintgram",
                                    crossover_type="full",
                                    crossover_rate=0.6,
                                    mutation_type="scramble")
        cipher_text = """
        Zc hdzq tr Zdytzir Gqstzir Zqltgtir, sezzdhgql ea nmq Dlztqr ea nmq
        Helnm, Fqhqldu ea nmq Aquty Uqftehr, dhg uecdu rqlodhn ne nmq nliq
        qzvqlel, Zdlsir Dilqutir. Adnmql ne d zilgqlqg reh, mirvdhg ne d
        zilgqlqg ktaq. Dhg T ktuu mdoq zc oqhfqdhsq, th nmtr utaq el nmq hqyn.
        """

        deciphered_text = gencipher.decipher(cipher_text, max_iter=20)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()

    print(deciphered_text)
    # print()
    # print(gencipher.history)


if __name__ == "__main__":
    main()

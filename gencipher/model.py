from random import random
from cProfile import Profile
import pstats
from numpy import inf

from fitness import NgramType, select_parent, generate_population, Ngram
from utils import decrypt
from crossover import Crossover, OX1, PMX, CX
from mutation import Mutation, insert, swap, inversion, scramble


class InvalidInputError(Exception):
    def __init__(
            self,
            var_name: str,
            var: any,
            var_class: Crossover | Mutation | NgramType
    ) -> None:
        """Raised when a variable is expected to have a valid value from
        the Crossover, Mutation, or NgramType Enum classes, but the
        provided value does not match any of the expected valid values.
        """
        super().__init__(
            f'Invalid {var_name}: "{var}".It should be one of '
            + ", ".join(f'"{value}"' for value in var_class.values()) + "."
        )


class GeneticDecipher:
    def __init__(
            self,
            ngram_type : str = "quadgram",
            n_population : int = 100,
            mutation_type : str = "scramble",
            mutation_rate : float = 0.01,
            crossover_type : str = "order-one",
            crossover_rate : float = 0.6
    ) -> None:
        self.ngram_type = ngram_type
        self.n_population = n_population
        self.mutation = self._set_mutation(mutation_type)
        self.mutation_rate = mutation_rate
        self.crossover = self._set_crossover(crossover_type)
        self.crossover_rate = crossover_rate

        self.ngram = Ngram(ngram_type)

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

    def decipher(
            self,
            cipher_text: str,
            max_iterations : int = 20
    ) -> str:
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

    @property
    def ngram_type(self):
        return self.__ngram_type

    @ngram_type.setter
    def ngram_type(self, ngram_type):
        if ngram_type in NgramType.values():
            self.__ngram_type = ngram_type
        else:
            raise InvalidInputError("ngram_type", ngram_type, NgramType)

    @staticmethod
    def _set_mutation(mutation_type):
        if mutation_type == Mutation.INSERT.value:
            return insert
        elif mutation_type == Mutation.INVERSION.value:
            return inversion
        elif mutation_type == Mutation.SWAP.value:
            return swap
        elif mutation_type == Mutation.SCRAMBLE.value:
            return scramble
        else:
            raise InvalidInputError("mutation", mutation_type, Mutation)

    @staticmethod
    def _set_crossover(crossover_type):
        if crossover_type == Crossover.CX.value:
            return CX
        elif crossover_type == Crossover.OX1.value:
            return OX1
        elif crossover_type == Crossover.PMX.value:
            return PMX
        else:
            raise InvalidInputError("crossover", crossover_type, Crossover)


def main():
    with Profile() as pr:
        gencipher = GeneticDecipher(ngram_type="quintgram")
        cipher_text = """
        Zc hdzq tr Zdytzir Gqstzir Zqltgtir, sezzdhgql ea nmq Dlztqr ea nmq
        Helnm, Fqhqldu ea nmq Aquty Uqftehr, dhg uecdu rqlodhn ne nmq nliq
        qzvqlel, Zdlsir Dilqutir. Adnmql ne d zilgqlqg reh, mirvdhg ne d
        zilgqlqg ktaq. Dhg T ktuu mdoq zc oqhfqdhsq, th nmtr utaq el nmq hqyn.
        """

        deciphered_text = gencipher.decipher(cipher_text)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()

    # print(deciphered_text)
    # print()
    # print(gencipher.history)


if __name__ == "__main__":
    main()

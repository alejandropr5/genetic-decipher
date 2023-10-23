from string import ascii_uppercase
from typing import Iterable, Union
from numpy import inf
from random import random

from gencipher.utils import CipherKey
from gencipher.mutation import Mutation
from gencipher.crossover import Crossover, ParentsLengthError
from gencipher.fitness import select_parent, Ngram


class GeneticDecipher(Crossover, Mutation):
    def __init__(
        self,
        ngram_type: str = "quadgram"
    ) -> None:
        """Initialize the GeneticDecipher class.

        Args:
            ngram_type (str, optional): The type of n-gram analysis to
            be used. Defaults to "quadgram."

        Summary:
        The GeneticDecipher class applies a genetic algorithm for
        cryptogram deciphering, using various strategies such as
        crossover, mutation, and fitness evaluation based on n-gram
        analysis. It aims to find the optimal decipher key for a
        given cryptogram.
        """
        self.ngram = Ngram(ngram_type)

    def FX(self, winner: CipherKey, loser: CipherKey) -> CipherKey:
        """Performs a full crossover (FX) operation on two parent
        strings to generate a offspring string.

        Args:
            winner (CipherKey): The parent with a higher fitness in
            solving the cryptogram, used as the first parent for
            crossover.
            loser (CipherKey): The parent with a lower fitness in
            solving the cryptogram, used as the second parent for
            crossover.

        Raises:
            ParentsLengthError: Raised if the lengths of winner and
            loser CipherKeys are not equal.

        Returns:
            CipherKey: The offspring CipherKey generated through the
            full crossover operation.
        """
        if len(winner) != len(loser):
            raise ParentsLengthError()

        target_fitness = self.population[winner]
        target_key = list(winner)
        source_key = list(loser)

        for idx in range(len(target_key)):
            if source_key[idx] != target_key[idx]:
                new_key = target_key[:]
                temp_idx = new_key.index(source_key[idx])
                new_key[idx], new_key[temp_idx] = source_key[idx], new_key[idx]
                new_key = CipherKey("".join(new_key))

                new_text = new_key.decode_cipher(self.cipher_text)
                new_fitness = self.ngram.compute_fitness(new_text)
                if new_fitness > target_fitness:
                    target_key = new_key
                    target_fitness = new_fitness
                target_key = list(target_key)

        return CipherKey("".join(target_key))

    def evolve_population(
        self,
        population: dict[CipherKey, float]
    ) -> dict[CipherKey, float]:
        """Evolves the population of candidate solutions through
        crossover and mutation.

        Args:
            population (dict): A dictionary representing the current
            population of candidate solutions, where keys are CipherKeys
            and values are their corresponding fitness scores (float).

        Returns:
            dict: A new population of candidate solutions after applying
            crossover and mutation, represented as a dictionary. Keys
            are CipherKeys, and values are their updated fitness scores
            (float).
        """
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
                new_text = new_key.decode_cipher(self.cipher_text)
                new_fitness = self.ngram.compute_fitness(new_text)
                if new_fitness < fitness_target:
                    new_key = winner
                    new_fitness = fitness_target
            if random() < self.mutation_rate:
                new_key = self.mutation(new_key)
                new_text = new_key.decode_cipher(self.cipher_text)
                new_fitness = self.ngram.compute_fitness(new_text)
            new_population[new_key] = new_fitness

        return new_population

    def decipher(
        self,
        cipher_text: str,
        max_iter: int = 20,
        n_population: int = 100,
        mutation_type: str = "scramble",
        crossover_type: str = "full",
        mutation_rate: float = 0.01,
        crossover_rate: float = 0.6
    ) -> str:
        """Deciphers a cryptogram using a genetic algorithm.

        Args:
            cipher_text (str): The cryptogram to be deciphered.
            max_iter (int, optional): The maximum number of iterations
            for the genetic algorithm. Defaults to 20.
            n_population (int, optional): The size of the candidate
            population for each iteration. Defaults to 100.
            mutation_type (str, optional): The type of mutation to be
            applied in the genetic algorithm. Defaults to "scramble."
            crossover_type (str, optional): The type of crossover to be
            applied in the genetic algorithm. Defaults to "full."
            mutation_rate (float, optional): The mutation rate,
            affecting the likelihood of applying mutation. Defaults to
            0.01.
            crossover_rate (float, optional): The crossover rate,
            affecting the likelihood of applying crossover. Defaults to
            0.6.

        Returns:
            str: The deciphered plaintext obtained through the genetic
            algorithm.
        """
        self.cipher_text = cipher_text
        self.n_population = n_population
        self._set_mutation(mutation_type)
        self._set_crossover(crossover_type)
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

        self.population = self.ngram.generate_population(self.cipher_text,
                                                         self.n_population)
        self.history: dict[str, list[Union[str, float]]] = {"key": [],
                                                            "score": [],
                                                            "text": []}
        best_key = (CipherKey(ascii_uppercase), -inf)

        deciphered_text = cipher_text
        for _ in range(max_iter):
            self.population = self.evolve_population(self.population)
            best_idx_key = max(self.population.items(), key=lambda x: x[1])

            if best_idx_key[1] > best_key[1]:
                best_key = best_idx_key
            deciphered_text = best_key[0].decode_cipher(self.cipher_text)

            self.history["key"].append(best_key[0])
            self.history["score"].append(best_key[1])
            self.history["text"].append(deciphered_text)

        return deciphered_text

    def decipher_generator(
        self,
        cipher_text: str,
        max_iter: int = 20,
        n_population: int = 100,
        mutation_type: str = "scramble",
        crossover_type: str = "full",
        mutation_rate: float = 0.01,
        crossover_rate: float = 0.6
    ) -> Iterable[tuple[str, float, str]]:
        self.cipher_text = cipher_text
        self.n_population = n_population
        self._set_mutation(mutation_type)
        self._set_crossover(crossover_type)
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

        self.population = self.ngram.generate_population(self.cipher_text,
                                                         self.n_population)
        best_key = (CipherKey(ascii_uppercase), -inf)

        deciphered_text = cipher_text
        for _ in range(max_iter):
            self.population = self.evolve_population(self.population)
            best_idx_key = max(self.population.items(), key=lambda x: x[1])

            if best_idx_key[1] > best_key[1]:
                best_key = best_idx_key
            deciphered_text = best_key[0].decode_cipher(self.cipher_text)

            yield best_key[0], best_key[1], deciphered_text

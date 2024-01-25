import re
import string
import random
import numpy as np
from typing import Iterator, Union

from gencipher.cipherkey import CipherKey
from gencipher.mutation import Mutation
from gencipher.crossover import Crossover, ParentsLengthError
from gencipher.ngram import Ngram, NgramType
from gencipher.utils import select_parent


class CipherTextLengthError(ValueError):
    """Inappropriate cipher text length."""
    def __init__(self):
        super().__init__("Invalid cipher text length. The cipher text must be "
                         "longer than the n-gram selected.")


class GeneticDecipher(Crossover, Mutation):
    def __init__(
        self,
        ngram_type: str = "quadgram"
    ) -> None:
        """Create a GeneticDecipher object.

        Args:
            ngram_type (str, optional): The type of n-gram analysis to
            be used. Defaults to "quadgram."
        """
        self.ngram = Ngram(ngram_type)

    def FX(self, winner: CipherKey, loser: CipherKey) -> CipherKey:
        """Perform a full crossover (FX) operation on two parent
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
                new_cipher_key = CipherKey("".join(new_key))

                new_text = new_cipher_key.decode_cipher(self.cipher_text)
                new_fitness = self.ngram.compute_fitness(new_text)
                if new_fitness > target_fitness:
                    target_key = new_key
                    target_fitness = new_fitness

        return CipherKey("".join(target_key))

    def evolve_population(
        self,
        population: dict[CipherKey, float]
    ) -> dict[CipherKey, float]:
        """Evolve the population of candidate solutions through
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

            if random.random() < self.crossover_rate:
                new_key = self.crossover(winner, loser)
                new_text = new_key.decode_cipher(self.cipher_text)
                new_fitness = self.ngram.compute_fitness(new_text)
                if new_fitness < fitness_target:
                    new_key = winner
                    new_fitness = fitness_target
            if random.random() < self.mutation_rate:
                new_key = self.mutation(new_key)
                new_text = new_key.decode_cipher(self.cipher_text)
                new_fitness = self.ngram.compute_fitness(new_text)
            new_population[new_key] = new_fitness

        return new_population

    def decipher(
        self,
        cipher_text: str,
        max_iter: int = 20,
        tolerance: float = 0.02,
        n_population: int = 100,
        mutation_type: str = "scramble",
        crossover_type: str = "full",
        mutation_rate: float = 0.01,
        crossover_rate: float = 0.6
    ) -> str:
        """Decipher a cryptogram using a genetic algorithm.

        Args:
            cipher_text (str): The cryptogram to be deciphered.
            max_iter (int, optional): The maximum number of iterations
            for the genetic algorithm. Defaults to 20.
            tolerance (float, optional): The algorithm stops when the
            fitness is within this tolerance. Defaults to 0.02
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
                                                            "fitness": [],
                                                            "text": []}
        best_key = (CipherKey(string.ascii_uppercase), -np.inf)

        deciphered_text = cipher_text
        for _ in range(max_iter):
            self.population = self.evolve_population(self.population)
            best_idx_key = max(self.population.items(), key=lambda x: x[1])

            if best_idx_key[1] > best_key[1]:
                best_key = best_idx_key
            deciphered_text = best_key[0].decode_cipher(self.cipher_text)

            ngram_count = self.ngram.ngram_count(deciphered_text)
            fitness_percentage = self.ngram.fitness_percentage(
                (best_key[1] / ngram_count)
            )

            self.history["key"].append(best_key[0])
            self.history["fitness"].append(fitness_percentage)
            self.history["text"].append(deciphered_text)

            if fitness_percentage >= 1 - tolerance:
                break

        return deciphered_text

    def decipher_generator(
        self,
        cipher_text: str,
        max_iter: int = 20,
        tolerance: float = 0.02,
        n_population: int = 100,
        mutation_type: str = "scramble",
        crossover_type: str = "full",
        mutation_rate: float = 0.01,
        crossover_rate: float = 0.6
    ) -> Iterator[tuple[str, float, str]]:
        """Decipher a cryptogram using a genetic algorithm.

        Args:
            cipher_text (str): The cryptogram to be deciphered.
            max_iter (int, optional): The maximum number of iterations
            for the genetic algorithm. Defaults to 20.
            tolerance (float, optional): The algorithm stops when the
            fitness is within this tolerance. Defaults to 0.02
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

        Yields:
            tuple[str, float, str]: A tuple containing the best
            deciphered key, its fitness as a percentage, and the
            corresponding deciphered text.
        """
        self.cipher_text = cipher_text
        self.n_population = n_population
        self._set_mutation(mutation_type)
        self._set_crossover(crossover_type)
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

        self.population = self.ngram.generate_population(self.cipher_text,
                                                         self.n_population)
        best_key = (CipherKey(string.ascii_uppercase), -np.inf)

        deciphered_text = cipher_text
        iteration = 0
        fitness_percentage = 0.0
        while iteration < max_iter and fitness_percentage < 1 - tolerance:
            self.population = self.evolve_population(self.population)
            best_idx_key = max(self.population.items(), key=lambda x: x[1])

            if best_idx_key[1] > best_key[1]:
                best_key = best_idx_key
            deciphered_text = best_key[0].decode_cipher(self.cipher_text)

            ngram_count = self.ngram.ngram_count(deciphered_text)
            fitness_percentage = self.ngram.fitness_percentage(
                (best_key[1] / ngram_count)
            )
            iteration += 1
            yield best_key[0], fitness_percentage, deciphered_text

    @property
    def cipher_text(self):
        return self.__cipher_text

    @cipher_text.setter
    def cipher_text(self, cipher_text):
        Ngram_list = NgramType.values()
        only_text = re.sub(r'[^A-Za-z]', '', cipher_text)

        if len(only_text) > Ngram_list.index(self.ngram.ngram_type):
            self.__cipher_text = cipher_text
        else:
            raise CipherTextLengthError

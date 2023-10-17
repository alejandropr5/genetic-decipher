from re import sub
import numpy as np
from enum import Enum
from glob import iglob
from math import log10
from pathlib import Path
from random import choices
from pickle import dump, load
from os.path import join, dirname, basename

from gencipher.utils import random_cipher_key, decrypt, InvalidInputError


class NgramType(Enum):
    MONOGRAM = "monogram"
    BIGRAM = "bigram"
    TRIGRAM = "trigram"
    QUADGRAM = "quadgram"
    QUINTGRAM = "quintgram"

    @classmethod
    def values(cls):
        """Retrieve the values of the NgramType enum class.

        Returns:
            Iterable[str]: An iterable containing the values of the
            NgramType enum as strings.
        """
        return [member.value for member in cls]


def ngrams_file_to_dictionary(
    file_path: str | Path,
    sep=" "
) -> dict[str, int]:
    """Reads the content of a n-gram text file, where each line consists
    of an n-gram string and its associated frequency, and converts it
    into a Python dictionary where n-gram strings are keys and their
    frequencies are integer values.

    Args:
        file_path (str | Path): The path to the n-gram text file.
        sep (str, optional): The separator used in the text file to
        separate n-gram strings and their frequencies. Defaults to " ".

    Returns:
        dict[ngram, frequency]: A Python dictionary where keys are
        n-gram strings, and values are their corresponding frequencies.
    """
    with open(file_path, "r") as file:
        content = file.read()

    ngram_strings = content.splitlines()

    ngrams_dictionary = {}
    for ngram in ngram_strings:
        ngram_pair = ngram.split(sep=sep)
        ngrams_dictionary[ngram_pair[0]] = int(ngram_pair[1])

    return ngrams_dictionary


def frequency_to_log_probability(ngrams_dictionary: dict[str, int]) -> None:
    """Converts frequency values in the n-gram dictionary to logarithmic
    probabilities.

    Args:
        ngrams_dictionary (dict[ngram, frequency]): A Python dictionary
        where keys are n-gram strings, and values are their
        corresponding frequencies.
    """
    total_frequency = sum(ngrams_dictionary.values())

    for key, value in ngrams_dictionary.items():
        ngrams_dictionary[key] = log10(value / total_frequency)

    ngrams_dictionary[0] = log10(0.01 / total_frequency)


def select_parent(population_fitness: dict[str, float]) -> str:
    """Selects a parent from a population based on their fitness scores
    using a weighted random selection.

    Args:
        population_fitness (dict): A dictionary containing fitness
        scores for individuals in the population.

    Returns:
        str: The selected parent chosen based on fitness scores.
    """
    values = list(population_fitness.values())
    values_arr = np.array(values)
    total_fitness = np.sum(values_arr)
    selection_probability = values_arr / total_fitness

    parent = choices(list(population_fitness),
                     weights=selection_probability,
                     k=1)

    return parent[0]


def ngrams_folder_to_dictionary_folder(
        source_folder: str | Path,
        output_folder: str | Path
) -> None:
    """Takes all n-gram score files (.txt) from the source folder,
    converts them into n-gram dictionaries with logarithmic
    probabilities and saves them in the output folder.

    Args:
        source_path (str | Path): The path to the source folder
        containing n-gram score text files.
        output_path (str | Path): The path to the output folder where
        n-gram dictionaries will be saved.
    """
    files = iglob(join(source_folder, "*.txt"))

    for file in files:
        file_name = basename(file).split(".")[0]

        ngrams_dictionary = ngrams_file_to_dictionary(file)
        frequency_to_log_probability(ngrams_dictionary)
        file = join(output_folder, f"{file_name}.dict")

        with open(file, "wb") as file_out:
            dump(ngrams_dictionary, file_out)


class Ngram:
    def __init__(self, ngram_type: str) -> None:
        """Initializes an Ngram object for a specified n-gram type.

        Args:
            ngram_type (str): The type of n-gram to initialize. It must
            be one of the following valid values: "monogram", "bigram,"
            "trigram", "quadgram", or "quintgram".
        """
        self.ngram_type = ngram_type
        parent_folder = join(dirname(__file__), "..")
        scores_folder = join(parent_folder, "ngrams_scores")
        file = join(scores_folder, f"english_{self.ngram_type}s.dict")
        with open(file, "rb") as file_in:
            self.scores = load(file_in)

        self.ngram_len = NgramType.values().index(self.ngram_type) + 1

    def compute_fitness(self, text: str) -> float:
        """Computes the fitness score of a given text based on n-gram
        frequencies.

        Args:
            text (str): The input text for which the fitness score is
            computed.

        Returns:
            float: The computed fitness score, representing the
            likelihood that the input text is an English text based
            on n-gram frequencies.
        """
        uppercase_text = text.upper()
        uppercase_only_text = sub(r'[^A-Z]', '', uppercase_text)
        fitness = 0.0

        for i in range(len(uppercase_only_text) - self.ngram_len + 1):
            ngram = uppercase_only_text[i : i + self.ngram_len]
            if ngram in self.scores:
                fitness += self.scores.get(ngram)
            else:
                fitness += self.scores.get(0)

        return fitness

    @property
    def ngram_type(self):
        return self.__ngram_type

    @ngram_type.setter
    def ngram_type(self, ngram_type):
        if ngram_type in NgramType.values():
            self.__ngram_type = ngram_type
        else:
            raise InvalidInputError("ngram_type", ngram_type, NgramType)

    def generate_population(
            self, cipher_text: str,
            n_population: int
    ) -> dict[str, float]:
        """Generates a population of random cipher keys and computes
        their fitness scores.

        Args:
            cipher_text (str): The cipher text to be decrypted by the
            generated cipher keys.
            n_population (int): The number of cipher keys to generate in
            the population.

        Returns:
            dict[str, float]: _description_
        """
        population = [random_cipher_key() for _ in range(n_population)]

        population_fitness = {}
        for key in population:
            decipher_text = decrypt(cipher_text, key)
            population_fitness[key] = self.compute_fitness(decipher_text)

        return population_fitness


def main():
    parent_folder = join(dirname(__file__), "..")
    folder_path = join(parent_folder, "ngrams_files")
    output_folder = join(parent_folder, "ngrams_scores")

    ngrams_folder_to_dictionary_folder(folder_path, output_folder)


if __name__ == "__main__":
    main()

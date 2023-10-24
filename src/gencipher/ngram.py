import os
import re
import glob
import math
import pickle
from typing import Union
from pathlib import Path
from importlib import resources


from gencipher.utils import InvalidInputError, InputType
from gencipher.cipherkey import CipherKey, random_cipher_key


class NgramType(InputType):
    """Collection of available types of n-grams for genetic
    algorithms.
    """
    MONOGRAM = "monogram"
    BIGRAM = "bigram"
    TRIGRAM = "trigram"
    QUADGRAM = "quadgram"
    QUINTGRAM = "quintgram"


class Ngram:
    _NGRAMS_SCORES = f"{resources.files('ngrams_scores')}"

    def __init__(
        self,
        ngram_type: str,
        scores_folder: Union[str, Path] = _NGRAMS_SCORES
    ) -> None:
        """Create a Ngram object for a specified n-gram type.

        Args:
            ngram_type (str): The type of n-gram to initialize. It must
            be one of the following valid values: "monogram", "bigram,"
            "trigram", "quadgram", or "quintgram".
            scores_folder (Union[str, Path]): The path to the
            folder containing the precomputed n-gram score pickled
            dictionaries. Defaults to "".
        """
        self.ngram_type = ngram_type

        file = os.path.join(scores_folder, f"english_{self.ngram_type}s.dict")
        with open(file, "rb") as file_in:
            self.scores = pickle.load(file_in)

        self.ngram_len = NgramType.values().index(self.ngram_type) + 1

    def compute_fitness(self, text: str) -> float:
        """Compute the fitness score of a given text based on n-gram
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
        uppercase_only_text = re.sub(r'[^A-Z]', '', uppercase_text)
        # uppercase_only_text = "".join(re.findall(r'[A-Z]', uppercase_text))
        fitness = 0.0

        for i in range(len(uppercase_only_text) - self.ngram_len + 1):
            top = i + self.ngram_len
            ngram = uppercase_only_text[i:top]
            if ngram in self.scores:
                fitness += self.scores[ngram]
            else:
                fitness += self.scores["0"]

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
    ) -> dict[CipherKey, float]:
        """Generate a population of random cipher keys and computes
        their fitness scores.

        Args:
            cipher_text (str): The cipher text to be decoded by the
            generated cipher keys.
            n_population (int): The number of cipher keys to generate in
            the population.

        Returns:
            dict[str, float]: _description_
        """
        population = [random_cipher_key() for _ in range(n_population)]

        population_fitness = {}
        for key in population:
            decipher_text = key.decode_cipher(cipher_text)
            population_fitness[key] = self.compute_fitness(decipher_text)

        return population_fitness

    def ngram_count(self, text: str) -> int:
        """Count the number of n-grams in the given text.

        Args:
            text (str): The input text from which n-grams will be
            counted.

        Returns:
            int: The count of n-grams ignoring non-alphabetical
            characters.
        """
        alpha_text = re.sub(r'[^A-Za-z]', '', text)
        return len(alpha_text) - self.ngram_len + 1


def _ngrams_file_to_dictionary(
    file_path: Union[str, Path],
    sep=" "
) -> dict[str, int]:  # pragma: no cover
    """Reads the content of a n-gram text file, where each line consists
    of an n-gram string and its associated frequency, and converts it
    into a Python dictionary where n-gram strings are keys and their
    frequencies are integer values.

    Args:
        file_path (Union[str, Path]): The path to the n-gram text file.
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


def _frequency_to_log_probability(
    ngrams_dictionary: dict[str, int]
) -> dict[str, float]:  # pragma: no cover
    """Convert frequency values in the n-gram dictionary to logarithmic
    probabilities.

    Args:
        ngrams_dictionary (dict[ngram, frequency]): A Python dictionary
        where keys are n-gram strings, and values are their
        corresponding frequencies.
    """
    total_frequency = sum(ngrams_dictionary.values())

    total_score = 0.0
    prob_dictionary = {}
    for key, value in ngrams_dictionary.items():
        prob_dictionary[key] = math.log10(value / total_frequency)
        total_score += prob_dictionary[key] * value

    prob_dictionary["0"] = math.log10(0.01 / total_frequency)
    prob_dictionary["fitness"] = total_score / total_frequency
    print(f"{len(list(prob_dictionary.keys())[0])}-gram:",
          prob_dictionary["fitness"])
    return prob_dictionary


def _ngrams_folder_to_dictionary_folder(
    source_folder: Union[str, Path],
    output_folder: Union[str, Path]
) -> None:  # pragma: no cover
    """Takes all n-gram score files (.txt) from the source folder,
    converts them into n-gram dictionaries with logarithmic
    probabilities and saves them in the output folder.

    Args:
        source_path (Union[str, Path]): The path to the source folder
        containing n-gram score text files.
        output_path (Union[str, Path]): The path to the output folder where
        n-gram dictionaries will be saved.
    """
    files = glob.iglob(os.path.join(source_folder, "*.txt"))

    for file in files:
        file_name = os.path.basename(file).split(".")[0]

        ngrams_dictionary = _ngrams_file_to_dictionary(file)
        prob_dictionary = _frequency_to_log_probability(ngrams_dictionary)
        print(prob_dictionary)
        file = os.path.join(output_folder, f"{file_name}.dict")

        with open(file, "wb") as file_out:
            pickle.dump(prob_dictionary, file_out)


def main():  # pragma: no cover
    parent_folder = os.path.join(os.path.dirname(__file__), "../..")
    folder_path = os.path.join(parent_folder, "data", "ngrams_files")
    output_folder = os.path.join(parent_folder, "data", "ngrams_scores")

    _ngrams_folder_to_dictionary_folder(folder_path, output_folder)


if __name__ == "__main__":  # pragma: no cover
    main()

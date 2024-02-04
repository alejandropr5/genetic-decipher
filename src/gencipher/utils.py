import enum
import random
import numpy as np
from typing import Union

from gencipher.cipherkey import CipherKey


class InputType(enum.Enum):
    """Create a custom collection of name/values pairs.
    It provides a method to retrieve the available values as strings.
    """
    @classmethod
    def values(cls):
        """Retrieve the values of the InputType enum class.

        Returns:
            Iterable[str]: An iterable containing the values of the
            InputType enum as strings.
        """
        return [member.value for member in cls]


class InvalidInputError(ValueError):
    """Input doesn't match any valid values from the InputType"""
    def __init__(
        self,
        var_name: str,
        var: Union[InputType, str],
        var_class: type[InputType]
    ) -> None:
        super().__init__(
            f"Invalid {var_name}: {var}. It should be one of ["
            + ", ".join(value for value in var_class.values()) + "]."
        )


def select_parent(population_fitness: dict[CipherKey, float]) -> CipherKey:
    """Select a parent from a population based on their fitness scores
    using a weighted random selection.

    Args:
        population_fitness (dict): A dictionary containing fitness
        scores for individuals in the population.

    Returns:
        CipherKey: The selected parent chosen based on fitness scores.
    """
    values = list(population_fitness.values())
    values_arr = np.array(values)
    total_fitness = np.sum(values_arr)
    selection_probability = values_arr / total_fitness

    parent = random.choices(list(population_fitness),
                            weights=selection_probability,
                            k=1)
    return parent[0]

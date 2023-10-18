from random import randint
from abc import ABC, abstractmethod

from gencipher.utils import InvalidInputError, InputType


class ParentsLengthError(ValueError):
    def __init__(self) -> None:
        """Raised when the lengths of parent strings for a crossover
        operation are not equal.
        """
        super().__init__("Parent strings must have equal lengths.")


class CrossoverType(InputType):
    OX1 = "order-one"
    PMX = "partially-mapped"
    CX = "cycle"
    FX = "full"


class Crossover(ABC):
    @staticmethod
    def OX1(parent1: str, parent2: str) -> str:
        """Performs order-one crossover (OX1) on two parent strings to
        generate a offspring string.

        Args:
            parent1 (str): The first parent string used for crossover.
            parent2 (str): The second parent string used for crossover.

        Raises:
            ParentsLengthError: Raised if the lengths of parent1 and
            parent2 are not equal.

        Returns:
            str: The offspring string generated through order-one crossover.
        """
        if len(parent1) != len(parent2):
            raise ParentsLengthError()

        length = len(parent1)
        start = randint(0, length)
        end = randint(start, length)

        offspring = list(parent1[start:end])
        offspring_length = len(offspring)

        parent_count = offspring_count = end
        while offspring_length < length:
            idx = parent_count % length
            parent_count += 1
            if parent2[idx] in offspring:
                continue
            else:
                offspring.insert(offspring_count % length, parent2[idx])
                offspring_count += 1
            offspring_length = len(offspring)

        return "".join(offspring)

    @staticmethod
    def PMX(parent1: str,
            parent2: str,
            start: int | None = None,
            end: int | None = None) -> str:
        """Performs partially mapped crossover (PMX) on two parent
        strings to generate a offspring string.

        Args:
            parent1 (str): The first parent string used for crossover.
            parent2 (str): The second parent string used for crossover.
            start (int | None, optional): First crossover point, if not
            provided, will be chosen randomly. Defaults to None.
            end (int | None, optional): Second crossover point, if not
            provided, will be chosen randomly. Defaults to None.

        Raises:
            ParentsLengthError: Raised if the lengths of parent1 and
            parent2 are not equal.

        Returns:
            str: The offspring string generated through partially mapped
            crossover.
        """
        if len(parent1) != len(parent2):
            raise ParentsLengthError()

        length = len(parent1)
        if start is None:
            start = randint(0, length)
        if end is None:
            end = randint(start, length)

        offspring = [""] * length
        mapping = {}
        for idx in range(start, end):
            offspring[idx] = parent1[idx]
            if parent2[idx] not in parent1[start:end]:
                mapping[parent2[idx]] = offspring[idx]

        for i, j in mapping.items():
            parent2_idx = parent2.index(j)
            while offspring[parent2_idx] != "":
                k = offspring[parent2_idx]
                parent2_idx = parent2.index(k)
            offspring[parent2_idx] = i

        offspring = list(map(lambda x, y: y if x == "" else x,
                             offspring,
                             parent2))

        return "".join(offspring)

    @staticmethod
    def CX(parent1: str, parent2: str) -> str:
        """Performs cycle crossover (CX) on two parent strings to
        generate a offspring string.

        Args:
            parent1 (str): The first parent string used for crossover.
            parent2 (str): The second parent string used for crossover.

        Raises:
            ParentsLengthError: Raised if the lengths of parent1 and
            parent2 are not equal.

        Returns:
            str: The offspring string generated through cycle crossover.
        """
        if len(parent1) != len(parent2):
            raise ParentsLengthError()

        length = len(parent1)
        offspring = [""] * length

        while "" in offspring:
            idx = offspring.index("")
            while offspring[idx] == "":
                offspring[idx] = parent2[idx]
                idx = parent1.index(parent2[idx])

        return "".join(offspring)

    @abstractmethod
    def FX(self, parent1: str, parent2: str) -> str:   # pragma: no cover
        """This method should implement the algorithm for a full
        crossover function, combining attributes of both parent strings
        to create a offspring.
        """
        pass

    def _set_crossover(self, crossover_type):
        if crossover_type == CrossoverType.CX.value:
            self.crossover = self.CX
        elif crossover_type == CrossoverType.OX1.value:
            self.crossover = self.OX1
        elif crossover_type == CrossoverType.PMX.value:
            self.crossover = self.PMX
        elif crossover_type == CrossoverType.FX.value:
            self.crossover = self.FX
        else:
            raise InvalidInputError("crossover", crossover_type, CrossoverType)

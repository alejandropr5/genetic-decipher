import random
from typing import Optional
from abc import ABC, abstractmethod

from gencipher.utils import InvalidInputError, InputType, CipherKey


class ParentsLengthError(ValueError):
    """Lengths of parents for a crossover operation are not equal."""
    def __init__(self) -> None:
        super().__init__("Parents must have equal lengths.")


class CrossoverType(InputType):
    """Collection of available methods for genetic crossover."""
    OX1 = "order-one"
    PMX = "partially-mapped"
    CX = "cycle"
    FX = "full"


class Crossover(ABC):
    """Abstract base class for crossover methods used in genetic
    algorithms.
    """
    @staticmethod
    def OX1(parent1: CipherKey, parent2: CipherKey) -> CipherKey:
        """Perform order-one crossover (OX1) on two parent strings to
        generate an offspring string.

        Args:
            parent1 (CipherKey): The first parent CipherKey used for
            crossover.
            parent2 (CipherKey): The second parent CipherKey used for
            crossover.

        Raises:
            ParentsLengthError: Raised if the lengths of parent1 and
            parent2 are not equal.

        Returns:
            CipherKey: The offspring generated through order-one
            crossover.
        """
        if len(parent1) != len(parent2):
            raise ParentsLengthError()

        length = len(parent1)
        start = random.randint(0, length)
        end = random.randint(start, length)

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

        return CipherKey("".join(offspring))

    @staticmethod
    def PMX(
        parent1: CipherKey,
        parent2: CipherKey,
        start: Optional[int] = None,
        end: Optional[int] = None
    ) -> CipherKey:
        """Perform partially mapped crossover (PMX) on two parent
        CipherKeys to generate an offspring CipherKey.

        Args:
            parent1 (CipherKey): The first parent CipherKey used for
            crossover.
            parent2 (CipherKey): The second parent CipherKey used for
            crossover.
            start (int, optional): First crossover point, if not
            provided, will be chosen randomly. Defaults to None.
            end (int, optional): Second crossover point, if not
            provided, will be chosen randomly. Defaults to None.

        Raises:
            ParentsLengthError: Raised if the lengths of parent1 and
            parent2 are not equal.

        Returns:
            str: The offspring generated through partially mapped
            crossover.
        """
        if len(parent1) != len(parent2):
            raise ParentsLengthError()

        length = len(parent1)
        if start is None:
            start = random.randint(0, length)
        if end is None:
            end = random.randint(start, length)

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

        return CipherKey("".join(offspring))

    @staticmethod
    def CX(parent1: CipherKey, parent2: CipherKey) -> CipherKey:
        """Perform cycle crossover (CX) on two parent CipherKeys to
        generate an offspring CipherKey.

        Args:
            parent1 (CipherKey): The first parent CipherKey used for
            crossover.
            parent2 (CipherKey): The second parent CipherKey used for
            crossover.

        Raises:
            ParentsLengthError: Raised if the lengths of parent1 and
            parent2 are not equal.

        Returns:
            CipherKey: The offspring generated through cycle crossover.
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

        return CipherKey("".join(offspring))

    @abstractmethod
    def FX(
        self,
        parent1: CipherKey,
        parent2: CipherKey
    ) -> CipherKey:   # pragma: no cover
        """This method should implement the algorithm for a full
        crossover function, combining attributes of both parent
        CipherKeys to create an offspring.
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

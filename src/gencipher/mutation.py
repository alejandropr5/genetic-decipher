import random

from gencipher.utils import InvalidInputError, InputType
from gencipher.cipherkey import CipherKey


class MutationType(InputType):
    """Collection of available methods for genetic mutation."""
    INSERT = "insert"
    SWAP = "swap"
    INVERSION = "inversion"
    SCRAMBLE = "scramble"


class Mutation:
    """Base class for mutation methods used in genetic algorithms."""
    @staticmethod
    def insert(parent: CipherKey) -> CipherKey:
        """Perform insert mutation on a parent CipherKey to generate a
        mutated CipherKey.

        Args:
            parent (CipherKey): The parent to undergo mutation.

        Returns:
            CipherKey: The mutated CipherKey.
        """
        parent_list = list(parent)
        pos1, pos2 = random.sample(range(len(parent_list)), 2)

        element = parent_list.pop(pos2)
        parent_list.insert(pos1 + 1, element)

        return CipherKey("".join(parent_list))

    @staticmethod
    def swap(parent: CipherKey) -> CipherKey:
        """Perform swap mutation on a parent CipherKey to generate a
        mutated CipherKey.

        Args:
            parent (CipherKey): The parent to undergo mutation.

        Returns:
            CipherKey: The mutated CipherKey.
        """
        parent_list = list(parent)
        pos1, pos2 = random.sample(range(len(parent_list)), 2)

        parent_list[pos1], parent_list[pos2] = (
            parent_list[pos2], parent_list[pos1]
        )

        return CipherKey("".join(parent_list))

    @staticmethod
    def inversion(parent: CipherKey) -> CipherKey:
        """Perform inversion mutation on a parent CipherKey to generate
        a mutated CipherKey.

        Args:
            parent (CipherKey): The parent to undergo mutation.

        Returns:
            CipherKey: The mutated CipherKey.
        """
        length = len(parent)
        start = random.randint(0, length)
        end = random.randint(start, length)

        parent_list = list(parent)
        parent_list[start:end] = reversed(parent_list[start:end])

        return CipherKey("".join(parent_list))

    @staticmethod
    def scramble(parent: CipherKey) -> CipherKey:
        """Perform scramble mutation on a parent CipherKey to generate
        a mutated CipherKey.

        Args:
            parent (CipherKey): The parent to undergo mutation.

        Returns:
            CipherKey: The mutated CipherKey.
        """
        length = len(parent)
        start = random.randint(0, length)
        end = random.randint(start, length)
        parent_list = list(parent)
        subList = parent_list[start:end]
        random.shuffle(subList)
        parent_list[start:end] = subList

        return CipherKey("".join(parent_list))

    def _set_mutation(self, mutation_type) -> None:
        if mutation_type == MutationType.INSERT.value:
            self.mutation = self.insert
        elif mutation_type == MutationType.INVERSION.value:
            self.mutation = self.inversion
        elif mutation_type == MutationType.SWAP.value:
            self.mutation = self.swap
        elif mutation_type == MutationType.SCRAMBLE.value:
            self.mutation = self.scramble
        else:
            raise InvalidInputError("mutation", mutation_type, MutationType)

from enum import Enum
from random import sample, randint, shuffle

from utils import InvalidInputError


class MutationType(Enum):
    INSERT = "insert"
    SWAP = "swap"
    INVERSION = "inversion"
    SCRAMBLE = "scramble"

    @classmethod
    def values(cls):
        return (member.value for member in cls)


class Mutation:
    @staticmethod
    def insert(parent: str) -> str:
        """Performs insert mutation on a parent string to generate a
        mutated string.

        Args:
            parent (str): The parent string to undergo mutation.

        Returns:
            str: The mutated string.
        """
        parent_list = list(parent)
        pos1, pos2 = sample(range(len(parent_list)), 2)

        element = parent_list.pop(pos2)
        parent_list.insert(pos1 + 1, element)

        return "".join(parent_list)

    @staticmethod
    def swap(parent: str) -> str:
        """Performs swap mutation on a parent string to generate a
        mutated string.

        Args:
            parent (str): The parent string to undergo mutation.

        Returns:
            str: The mutated string.
        """
        parent_list = list(parent)
        pos1, pos2 = sample(range(len(parent_list)), 2)

        parent_list[pos1], parent_list[pos2] = (
            parent_list[pos2], parent_list[pos1]
        )

        return "".join(parent_list)

    @staticmethod
    def inversion(parent: str) -> str:
        """Performs inversion mutation on a parent string to generate a
        mutated string.

        Args:
            parent (str): The parent string to undergo mutation.

        Returns:
            str: The mutated string.
        """
        length = len(parent)
        start = randint(0, length)
        end = randint(start, length)

        parent_list = list(parent)
        parent_list[start:end] = reversed(parent_list[start:end])

        return "".join(parent_list)

    @staticmethod
    def scramble(parent: str) -> str:
        """Performs scramble mutation on a parent string to generate a
        mutated string.

        Args:
            parent (str): The parent string to undergo mutation.

        Returns:
            str: The mutated string.
        """
        length = len(parent)
        start = randint(0, length)
        end = randint(start, length)
        parent_list = list(parent)
        subList = parent_list[start:end]
        shuffle(subList)
        parent_list[start:end] = subList

        return "".join(parent_list)

    def _set_mutation(self, mutation_type):
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


def main():
    parent = list("123456789")

    print(parent)
    print()
    mut = Mutation()
    print(list(mut.insert(parent)))
    print(list(mut.swap(parent)))
    print(list(mut.inversion(parent)))
    print(list(mut.scramble(parent)))


if __name__ == "__main__":
    main()

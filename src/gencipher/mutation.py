from random import sample, randint, shuffle

from gencipher.utils import InvalidInputError, InputType


class MutationType(InputType):
    INSERT = "insert"
    SWAP = "swap"
    INVERSION = "inversion"
    SCRAMBLE = "scramble"

    @classmethod
    def values(cls):
        """Retrieve the values of the MutationType enum class.

        Returns:
            Iterable[str]: An iterable containing the values of the
            MutationType enum as strings.
        """
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

    def _set_mutation(self, mutation_type) -> None:
        """Set the mutation function based on the provided mutation
        type.

        Args:
            mutation_type (str): The mutation type as a string.

        Raises:
            InvalidInputError: Raised if the provided mutation_type is
            not one of the valid mutation types defined in MutationType.
        """
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

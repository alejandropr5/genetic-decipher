from random import sample, randint, shuffle

from gencipher.utils import CipherKey, InvalidInputError, InputType


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
    def insert(parent: CipherKey) -> CipherKey:
        """Performs insert mutation on a parent CipherKey to generate a
        mutated CipherKey.

        Args:
            parent (CipherKey): The parent to undergo mutation.

        Returns:
            CipherKey: The mutated CipherKey.
        """
        parent_list = list(parent)
        pos1, pos2 = sample(range(len(parent_list)), 2)

        element = parent_list.pop(pos2)
        parent_list.insert(pos1 + 1, element)

        return CipherKey("".join(parent_list))

    @staticmethod
    def swap(parent: CipherKey) -> CipherKey:
        """Performs swap mutation on a parent CipherKey to generate a
        mutated CipherKey.

        Args:
            parent (CipherKey): The parent to undergo mutation.

        Returns:
            CipherKey: The mutated CipherKey.
        """
        parent_list = list(parent)
        pos1, pos2 = sample(range(len(parent_list)), 2)

        parent_list[pos1], parent_list[pos2] = (
            parent_list[pos2], parent_list[pos1]
        )

        return CipherKey("".join(parent_list))

    @staticmethod
    def inversion(parent: CipherKey) -> CipherKey:
        """Performs inversion mutation on a parent CipherKey to generate
        a mutated CipherKey.

        Args:
            parent (CipherKey): The parent to undergo mutation.

        Returns:
            CipherKey: The mutated CipherKey.
        """
        length = len(parent)
        start = randint(0, length)
        end = randint(start, length)

        parent_list = list(parent)
        parent_list[start:end] = reversed(parent_list[start:end])

        return CipherKey("".join(parent_list))

    @staticmethod
    def scramble(parent: CipherKey) -> CipherKey:
        """Performs scramble mutation on a parent CipherKey to generate
        a mutated CipherKey.

        Args:
            parent (CipherKey): The parent to undergo mutation.

        Returns:
            CipherKey: The mutated CipherKey.
        """
        length = len(parent)
        start = randint(0, length)
        end = randint(start, length)
        parent_list = list(parent)
        subList = parent_list[start:end]
        shuffle(subList)
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

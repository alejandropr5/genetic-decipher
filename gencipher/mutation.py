from enum import Enum
from random import sample, randint, shuffle


class Mutation(Enum):
    INSERT = "insert"
    SWAP = "swap"
    INVERSION = "inversion"
    SCRAMBLE = "scramble"

    @classmethod
    def values(cls):
        return (member.value for member in cls)


def insert(parent: str) -> str:
    """Performs insert mutation on a parent string to generate a mutated
    string.

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


def swap(parent: str) -> str:
    """Performs swap mutation on a parent string to generate a mutated
    string.

    Args:
        parent (str): The parent string to undergo mutation.

    Returns:
        str: The mutated string.
    """
    parent_list = list(parent)
    pos1, pos2 = sample(range(len(parent_list)), 2)

    parent_list[pos1], parent_list[pos2] = parent_list[pos2], parent_list[pos1]

    return "".join(parent_list)


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
    print(start, end)
    parent_list = list(parent)
    subList = parent_list[start:end]
    shuffle(subList)
    parent_list[start:end] = subList

    return "".join(parent_list)


def main():
    parent = list("123456789")

    print(parent)
    print()
    print(list(insert(parent)))
    print(list(swap(parent)))
    print(list(inversion(parent)))
    print(list(scramble(parent)))


if __name__ == "__main__":
    main()

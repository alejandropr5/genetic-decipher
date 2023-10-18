from re import match
from enum import Enum
from io import StringIO
from random import shuffle
from string import ascii_uppercase, ascii_lowercase


class InputType(Enum):
    @classmethod
    def values(cls):
        """Retrieve the values of the InputType enum class.

        Returns:
            Iterable[str]: An iterable containing the values of the
            InputType enum as strings.
        """
        return [member.value for member in cls]


class InvalidInputError(ValueError):
    def __init__(
        self,
        var_name: str,
        var: InputType,
        var_class: type[InputType]
    ) -> None:
        """Raised when a variable is expected to have a valid value from
        the Crossover, Mutation, or NgramType Enum classes, but the
        provided value does not match any of the expected valid values.
        """
        super().__init__(
            f'Invalid {var_name}: "{var}".It should be one of '
            + ", ".join(f'"{value}"' for value in var_class.values()) + "."
        )


def random_cipher_key() -> str:
    """Generates a random substitution cipher key.

    Returns:
        str: A randomly shuffled string representing a substitution
        cipher key.
    """
    cipher_key_list = list(ascii_uppercase)
    shuffle(cipher_key_list)
    cipher_key_str = "".join(cipher_key_list)
    return cipher_key_str


def encrypt(text: str, cipher_key: str | list[str]) -> str:
    """Substitutes characters in the input text using a provided
    substitution cipher key.

    Args:
        text (str): The input text to be encrypted.
        cipher_key (str): The substitution cipher key used for character
        mapping.

    Returns:
        str: The text with characters substituted based on the provided
        cipher key.
    """
    cipher_text = ""
    for char in text:
        if match('[A-Z]', char):
            cipher_text += cipher_key[(ord(char) - ord('A'))]
        elif match('[a-z]', char):
            cipher_text += cipher_key[(ord(char) - ord('a'))].lower()
        else:
            cipher_text += char

    return cipher_text


def encrypt_deprecated(text: str, cipher_key: str | list[str]) -> str:
    """Substitutes characters in the input text using a provided
    substitution cipher key.

    Args:
        text (str): The input text to be encrypted.
        cipher_key (str): The substitution cipher key used for character
        mapping.

    Returns:
        str: The text with characters substituted based on the provided
        cipher key.
    """
    cipher_text = StringIO()
    for char in text:
        if match('[A-Z]', char):
            cipher_text.write(cipher_key[(ord(char) - ord('A'))])
        elif match('[a-z]', char):
            cipher_text.write(cipher_key[(ord(char) - ord('a'))].lower())
        else:
            cipher_text.write(char)

    return cipher_text.getvalue()


def decrypt_deprecated(text: str, cipher_key: str | list[str]) -> str:
    """Substitutes characters in the input text using a provided
    substitution cipher key.

    Args:
        text (str): The input text to be decrypted.
        cipher_key (str): The substitution cipher key used for character
        mapping.

    Returns:
        str: The text with characters substituted based on the provided
        cipher key.
    """
    plain_text = StringIO()
    for char in text:
        if char in ascii_uppercase:
            plain_text.write(
                chr(cipher_key.index(char.upper()) + ord('A'))
            )
        elif char in ascii_lowercase:
            plain_text.write(
                chr(cipher_key.index(char.upper()) + ord('a'))
            )
        else:
            plain_text.write(char)

    return plain_text.getvalue()


def decrypt(text: str, cipher_key: str | list[str]) -> str:
    """Substitutes characters in the input text using a provided
    substitution cipher key.

    Args:
        text (str): The input text to be decrypted.
        cipher_key (str): The substitution cipher key used for character
        mapping.

    Returns:
        str: The text with characters substituted based on the provided
        cipher key.
    """
    plain_text = ""
    for char in text:
        if char in ascii_uppercase:
            plain_text += chr(cipher_key.index(char.upper()) + ord('A'))
        elif char in ascii_lowercase:
            plain_text += chr(cipher_key.index(char.upper()) + ord('a'))
        else:
            plain_text += char

    return plain_text

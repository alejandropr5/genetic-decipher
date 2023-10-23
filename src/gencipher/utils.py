from enum import Enum
from random import shuffle
from typing import Self
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


class InvalidInputError(Exception):
    def __init__(
        self,
        var_name: str,
        var: InputType,
        var_class: type[InputType]
    ) -> None:
        """Raised when a variable is expected to have a valid value from
        the InputType classes, but the provided value does not match any of
        the expected valid values.
        """
        super().__init__(
            f'Invalid {var_name}: "{var}".It should be one of '
            + ", ".join(f'"{value}"' for value in var_class.values()) + "."
        )


class InvalidCipherKey(Exception):
    def __init__(self):
        super().__init__("Invalid cipher key. The key must contain all"
                         "letters of the english alphabet.")


class CipherKey(str):
    """Create a new CipherKey object from the given string.


    This class extends the functionality of Python strings to represent
    cipher keys used in decryption. It provides methods for encoding and
    decoding plain texts using the cipher key.
    """
    def __new__(cls, value: str) -> Self:
        cls._check_value(value)
        return super().__new__(cls, value)

    def __init__(self, value: str) -> None:
        camel_key = value.lower() + value.upper()
        camel_alphabet = ascii_lowercase + ascii_uppercase
        self._encode_table = str.maketrans(camel_alphabet, camel_key)
        self._decode_table = str.maketrans(camel_key, camel_alphabet)
        super().__init__()

    @staticmethod
    def _check_value(value: str):
        if type(value) is not str:
            raise ValueError('Not a str type')
        if sorted(value.upper()) != sorted(ascii_uppercase):
            raise InvalidCipherKey()

    def encode_cipher(self, plain_text: str) -> str:
        """Encodes plain text using the cipher key.

        Args:
            plain_text (str): The plain text to be encoded.

        Returns:
            str: The encoded cipher text.
        """
        return plain_text.translate(self._encode_table)

    def decode_cipher(self, cipher_text: str) -> str:
        """Decodes cipher text using the cipher key.

        Args:
            cipher_text (str): The cipher text to be decoded.

        Returns:
            str: The decoded plain text.
        """
        return cipher_text.translate(self._decode_table)


def random_cipher_key() -> CipherKey:
    """Generates a random substitution cipher key.

    Returns:
        CipherKey: A randomly shuffled CipherKey.
    """
    cipher_key_list = list(ascii_uppercase)
    shuffle(cipher_key_list)
    cipher_key_str = CipherKey("".join(cipher_key_list))
    return cipher_key_str

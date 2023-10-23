import string
import random
from typing import TypeVar, Type


class InvalidCipherKey(ValueError):
    """Inappropriate cipher key value"""
    def __init__(self):
        super().__init__("Invalid cipher key. The key must contain all"
                         "letters of the english alphabet.")


TCipherKey = TypeVar("TCipherKey", bound="CipherKey")


class CipherKey(str):
    """Create a new CipherKey object from the given string.


    This class extends the functionality of Python strings to represent
    cipher keys used in decryption. It provides methods for encoding and
    decoding plain texts using the cipher key.
    """
    def __new__(cls: Type[TCipherKey], value: str) -> TCipherKey:
        cls._check_value(value)
        return super().__new__(cls, value)

    def __init__(self, value: str) -> None:
        camel_key = value.lower() + value.upper()
        camel_alphabet = string.ascii_lowercase + string.ascii_uppercase
        self._encode_table = str.maketrans(camel_alphabet, camel_key)
        self._decode_table = str.maketrans(camel_key, camel_alphabet)
        super().__init__()

    @staticmethod
    def _check_value(value: str):
        if type(value) is not str:
            raise ValueError('Not a str type')
        if sorted(value.upper()) != sorted(string.ascii_uppercase):
            raise InvalidCipherKey()

    def encode_cipher(self, plain_text: str) -> str:
        """Encode plain text using the cipher key.

        Args:
            plain_text (str): The plain text to be encoded.

        Returns:
            str: The encoded cipher text.
        """
        return plain_text.translate(self._encode_table)

    def decode_cipher(self, cipher_text: str) -> str:
        """Decode cipher text using the cipher key.

        Args:
            cipher_text (str): The cipher text to be decoded.

        Returns:
            str: The decoded plain text.
        """
        return cipher_text.translate(self._decode_table)


def random_cipher_key() -> CipherKey:
    """Generate a random substitution cipher key.

    Returns:
        CipherKey: A randomly shuffled CipherKey.
    """
    cipher_key_list = list(string.ascii_uppercase)
    random.shuffle(cipher_key_list)
    cipher_key_str = CipherKey("".join(cipher_key_list))
    return cipher_key_str

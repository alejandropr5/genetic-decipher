from string import ascii_uppercase
import pytest

from gencipher import utils
from gencipher.fitness import Ngram


def test_cipher_key_exceptions():
    with pytest.raises(ValueError):
        utils.CipherKey(1)

    with pytest.raises(utils.InvalidCipherKey):
        utils.CipherKey("test")


def test_random_cipher_key():
    key = utils.random_cipher_key()

    assert isinstance(key, str)
    assert len(key) == len(ascii_uppercase)
    assert set(key) == set(ascii_uppercase)


def test_cipher_key_encode_cipher():
    # Test with a simple substitution key, rotating one letter
    cipher_key = utils.CipherKey("BCDEFGHIJKLMNOPQRSTUVWXYZA")

    text = "HELLO"
    encrypted_text = cipher_key.encode_cipher(text)
    assert encrypted_text == "IFMMP"

    # Test with non-alphabetic characters
    text = "123!@#"
    encrypted_text = cipher_key.encode_cipher(text)
    assert encrypted_text == "123!@#"

    # Test with lowercase text
    text = "world"
    encrypted_text = cipher_key.encode_cipher(text)
    assert encrypted_text == "xpsme"

    # Test with lowercase text, uppercase text and non-alphabetic
    # characters
    text = "HELLO world!"
    encrypted_text = cipher_key.encode_cipher(text)
    assert encrypted_text == "IFMMP xpsme!"


def test_cipher_key_decode_cipher():
    # Test with a simple substitution key, rotating one letter
    cipher_key = utils.CipherKey("BCDEFGHIJKLMNOPQRSTUVWXYZA")

    text = "IFMMP"
    encrypted_text = cipher_key.decode_cipher(text)
    assert encrypted_text == "HELLO"

    # Test with non-alphabetic characters
    text = "123!@#"
    encrypted_text = cipher_key.decode_cipher(text)
    assert encrypted_text == "123!@#"

    # Test with lowercase text
    text = "xpsme"
    encrypted_text = cipher_key.decode_cipher(text)
    assert encrypted_text == "world"

    # Test with lowercase text, uppercase text and non-alphabetic
    # characters
    text = "IFMMP xpsme!"
    encrypted_text = cipher_key.decode_cipher(text)
    assert encrypted_text == "HELLO world!"


def test_input_error(monogram_gencipher):
    invalid_input = "invalid_input"

    # Test InvalidInputError in Ngram class
    with pytest.raises(utils.InvalidInputError):
        Ngram(ngram_type=invalid_input, scores_folder="")

    # Test InvalidInputError in Mutation class
    with pytest.raises(utils.InvalidInputError):
        monogram_gencipher.decipher(cipher_text="",
                                    mutation_type=invalid_input)

    # Test InvalidInputError in Crossover class
    with pytest.raises(utils.InvalidInputError):
        monogram_gencipher.decipher(cipher_text="",
                                    crossover_type=invalid_input)

import pytest
import string

from gencipher.cipherkey import CipherKey, InvalidCipherKey, random_cipher_key


def test_cipher_key_exceptions():
    with pytest.raises(ValueError):
        CipherKey(1)

    with pytest.raises(InvalidCipherKey):
        CipherKey("test")


def test_random_cipher_key():
    key = random_cipher_key()

    assert isinstance(key, str)
    assert len(key) == len(string.ascii_uppercase)
    assert set(key) == set(string.ascii_uppercase)


def test_cipher_key_encode_cipher():
    # Test with a simple substitution key, rotating one letter
    cipher_key = CipherKey("BCDEFGHIJKLMNOPQRSTUVWXYZA")

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
    cipher_key = CipherKey("BCDEFGHIJKLMNOPQRSTUVWXYZA")

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

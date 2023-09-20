from re import match
from random import shuffle
from string import ascii_uppercase


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


def encrypt(text: str, cipher_key: str) -> str:
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


def decrypt(text: str, cipher_key: str) -> str:
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
    decipher_text = ""
    for char in text:
        if match('[A-Z]', char):
            decipher_text += chr(cipher_key.index(char.upper()) + ord('A'))
        elif match('[a-z]', char):
            decipher_text += chr(cipher_key.index(char.upper()) + ord('a'))
        else:
            decipher_text += char

    return decipher_text


def main():
    cipher_key = random_cipher_key()

    print(ascii_uppercase)
    print(cipher_key)

    text = "Hello World!!"

    cipher_text = encrypt(text, cipher_key)

    decipher_text = decrypt(cipher_text, cipher_key)

    print(text)
    print(cipher_text)
    print(decipher_text)


if __name__ == "__main__":
    main()

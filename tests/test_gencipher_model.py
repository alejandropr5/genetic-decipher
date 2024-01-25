import pytest
from gencipher.model import GeneticDecipher, CipherTextLengthError


def test_decipher_method():
    gencipher = GeneticDecipher()

    # Test decipher method with
    cipher_text = (
        "Rbo rpktigo vcrb bwucja wj kloj hcjd, km sktpqo, cq rbwr loklgo "
        "vcgg cjqcqr kj skhcja wgkja wjd rpycja rk ltr rbcjaq cj cr."
    )

    deciphered_text = gencipher.decipher(cipher_text,
                                         max_iter=20,
                                         tolerance=0.1)

    assert len(deciphered_text) == len(deciphered_text)
    assert (gencipher.ngram.compute_fitness(deciphered_text) >=
            gencipher.ngram.compute_fitness(cipher_text))


def test_decipher_generator_method():
    gencipher = GeneticDecipher()

    # Test decipher_generator method
    cipher_text = (
        "Rbo rpktigo vcrb bwucja wj kloj hcjd, km sktpqo, cq rbwr loklgo "
        "vcgg cjqcqr kj skhcja wgkja wjd rpycja rk ltr rbcjaq cj cr."
    )

    decipher_generator = gencipher.decipher_generator(
        cipher_text,
        max_iter=20,
        crossover_type="partially-mapped"
    )

    for _, _, deciphered_text in decipher_generator:
        assert len(deciphered_text) == len(cipher_text)
        assert (gencipher.ngram.compute_fitness(deciphered_text) >=
                gencipher.ngram.compute_fitness(cipher_text))


def test_cipher_text_error():
    gencipher = GeneticDecipher(ngram_type="bigram")
    cipher_text = "a"

    with pytest.raises(CipherTextLengthError):
        gencipher.decipher(cipher_text)

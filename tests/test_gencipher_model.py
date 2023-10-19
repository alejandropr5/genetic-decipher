from gencipher.model import GeneticDecipher


def test_decipher_method():
    gencipher = GeneticDecipher()

    # Test decipher method with a known cipher text
    cipher_text = (
        "Rbo rpktigo vcrb bwucja wj kloj hcjd, km sktpqo, cq rbwr loklgo "
        "vcgg cjqcqr kj skhcja wgkja wjd rpycja rk ltr rbcjaq cj cr."
    )
    decoded_text = (
        "The trouble with having an open mind, of course, is that people "
        "will insist on coming along and trying to put things in it."
    )
    deciphered_text = gencipher.decipher(cipher_text,
                                         max_iter=20,
                                         crossover_type="partially-mapped")

    assert len(deciphered_text) == len(decoded_text)
    assert (abs(gencipher.ngram.compute_fitness(deciphered_text)) >
            abs(gencipher.ngram.compute_fitness(decoded_text)))

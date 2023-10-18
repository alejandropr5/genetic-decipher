import pytest
from gencipher.model import GeneticDecipher


@pytest.mark.xfail
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
                                         max_iter=20)
    assert deciphered_text == decoded_text

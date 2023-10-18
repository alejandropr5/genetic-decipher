import pytest


@pytest.mark.parametrize("mutation_type", [
    "insert",
    "swap",
    "inversion",
    "scramble"
])
def test_mutation_methods(mutation_type, monogram_gencipher):
    monogram_gencipher.decipher(cipher_text="",
                                mutation_type=mutation_type,
                                max_iter=0)

    parent = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    mutated = monogram_gencipher.mutation(parent)
    assert sorted(mutated) == sorted(parent)

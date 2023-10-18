import pytest

from gencipher.model import GeneticDecipher


@pytest.fixture(scope="session")
def monogram_gencipher():
    return GeneticDecipher("monogram")

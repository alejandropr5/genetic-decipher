from subbreaker.breaker import Breaker
from gencipher.model import GeneticDecipher
from os.path import join, dirname
from time import perf_counter
from cProfile import Profile
import pstats


_cipher_text = """
Zc hdzq tr Zdytzir Gqstzir Zqltgtir, sezzdhgql ea nmq Dlztqr ea nmq
Helnm, Fqhqldu ea nmq Aquty Uqftehr, dhg uecdu rqlodhn ne nmq nliq
qzvqlel, Zdlsir Dilqutir. Adnmql ne d zilgqlqg reh, mirvdhg ne d
zilgqlqg ktaq. Dhg T ktuu mdoq zc oqhfqdhsq, th nmtr utaq el nmq hqyn.
"""


def main():
    # start1 = perf_counter()
    # file = join(dirname(__file__), "ngrams_scores", "EN.json")
    # with open(file, "rb") as file_in:
        # breaker = Breaker(file_in)
    # result = breaker.break_cipher(_cipher_text)
    # end1 = perf_counter()

    # start2 = perf_counter()
    # gencipher = GeneticDecipher(crossover_rate=0.6)
    # pt = gencipher.decipher(_cipher_text)
    # end2 = perf_counter()

    # print(end1 - start1)
    # print(result.plaintext)
    # print()
    # print(end2 - start2)
    # print(pt)

    with Profile() as pr:
        gencipher = GeneticDecipher()
        gencipher.decipher(_cipher_text)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()


if __name__ == "__main__":
    main()

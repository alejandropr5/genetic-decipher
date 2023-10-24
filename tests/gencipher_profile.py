import cProfile
import pstats

from gencipher.model import GeneticDecipher


def main():
    with cProfile.Profile() as pr:
        gencipher = GeneticDecipher("quadgram")
        cipher_text = (
            "Zc hdzq tr Zdytzir Gqstzir Zqltgtir, sezzdhgql ea nmq Dlztqr ea "
            "nmq Helnm, Fqhqldu ea nmq Aquty Uqftehr, dhg uecdu rqlodhn ne "
            "nmq nliq qzvqlel, Zdlsir Dilqutir. Adnmql ne d zilgqlqg reh, "
            "mirvdhg ne d zilgqlqg ktaq. Dhg T ktuu mdoq zc oqhfqdhsq, th "
            "nmtr utaq el nmq hqyn."
        )
        print(gencipher.decipher(cipher_text, tolerance=0.034))

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    # stats.dump_stats(filename="needs_profiling.prof")


if __name__ == "__main__":
    main()
    # from itertools import tee
    # from collections import deque
    # from itertools import islice
    # def quadwise(iterable):
    #     "s -> (s0,s1,s2), (s1,s2,s3), (s2, s3,s4), ..."
    #     a, b, c, d = tee(iterable, 4)
    #     next(b)
    #     next(c)
    #     next(c)
    #     next(d)
    #     next(d)
    #     next(d)
    #     return zip(a, b, c)

    # def sliding_window(iterable, n):
    #     it = iter(iterable)
    #     window = deque(islice(it, n - 1), maxlen=n)
    #     for x in it:
    #         window.append(x)
    #         yield tuple(window)

    # with cProfile.Profile() as pr:
    #     text = "abcdefghijklmnopqrstuvwxyz"
    #     print(list(quadwise(text)))
    #     print(list(sliding_window(text, 2)))
    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()

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
        print(gencipher.decipher(cipher_text))

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    # stats.dump_stats(filename="needs_profiling.prof")


if __name__ == "__main__":
    main()

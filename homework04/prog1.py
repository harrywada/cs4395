import nltk
from nltk import word_tokenize
from nltk.util import ngrams
import pickle
import sys

PACKAGES: list[str] = [ "punkt" ]

def grams(path: str) -> tuple[dict[str, int], dict[str, int]]:
    unigrams: list[str] = []
    with open(path) as file:
        for line in file:
            unigrams += word_tokenize(line.rstrip("\n"))
    bigrams = list(ngrams(unigrams, 2))

    unigram_counts = { g: unigrams.count(g) for g in set(unigrams) }
    bigram_counts = { g: bigrams.count(g) for g in set(bigrams) }
    return ( unigram_counts, bigram_counts )

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Must provide paths to training files", file=sys.stderr)
        sys.exit(1)

    for package in PACKAGES:
        nltk.download(package, download_dir="./.venv/nltk_data/", quiet=True)

    for path in sys.argv[1:]:
        try:
            ( unigrams, bigrams ) = grams(path)
        except OSError as err:
            print(f"Cannot open file: {err.strerror}", file=sys.stderr)
            sys.exit(1)

        try:
            with open(f"{path}_unigrams.pickle", "wb") as file:
                pickle.dump(unigrams, file)
            with open(f"{path}_bigrams.pickle", "wb") as file:
                pickle.dump(bigrams, file)
        except OSError as err:
            print(f"Can't create pickle file: {err.strerror}", file=sys.stderr)
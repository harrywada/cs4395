import nltk
from nltk import word_tokenize
from nltk.util import ngrams
import pickle
import sys

PACKAGES: list[str] = [ "punkt" ]

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Need test file path and pickle file stems", file=sys.stderr)
        sys.exit(1)

    for package in PACKAGES:
        nltk.download(package, download_dir="./.venv/nltk_data/", quiet=True)

    for stem in sys.argv[2:]:
        try:
            with open(f"{stem}_unigrams.pickle", "rb") as file:
                ref_unigrams = pickle.load(file)
            with open(f"{stem}_bigrams.pickle", "rb") as file:
                ref_bigrams = pickle.load(file)

            # Only open file to minimize indentation; remember to close.
            tests = open(sys.argv[1])

            for line in tests:
                line = line.rstrip()
                test_unigrams = word_tokenize(line)
                test_bigrams = list(ngrams(test_unigrams, 2))

                N = len(test_unigrams)
                V = len(set(test_unigrams))
                p_gt = 1
                p_laplace = 1

                for b in test_bigrams:
                    n = ref_bigrams[b] if b in ref_bigrams else 0
                    n_gt = ref_bigrams[b] if b in ref_bigrams else 1 / N
                    d = ref_unigrams[b[0]] if b[0] in ref_unigrams else 0
                    if d == 0:
                        p_gt = p_gt * (1 / N)
                    else:
                        p_gt = p_gt * (n_gt / d)
                    p_laplace = p_laplace * ((n + 1) / (d + V))

                print(f"{p_laplace * 100}% probability for {stem}: {line}")

            tests.close()
        except OSError as err:
            print(f"Can't read file: {err.strerror}", file=sys.stderr)
            sys.exit(1)
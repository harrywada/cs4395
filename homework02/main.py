import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import operator
import random
import sys

PACKAGES = [ "punkt", "stopwords", "wordnet", "averaged_perceptron_tagger" ]

def guessing_game(words: list[str], points: int = 5) -> None:
    print("Let's play a word guessing game!")

    word = random.choice(words)
    show = [ False for _ in word ]

    while points > 0:
        print(" ".join([ word[i] if show[i] else "_"
                         for i in range(0, len(word)) ]))

        if set(show) == { True }:
            print("You solved it!")
            print()
            print(f"Current score: {points}")
            print()
            word = random.choice(words) # TODO Exclude current word
            show = [ False for _ in word ]
            continue

        guess = input("Guess a letter: ")[0] # FIXME IndexError on empty input

        if guess == "!":
            return
        elif guess in word:
            show = [ True if show[i] or word[i] == guess else False
                     for i in range(0, len(show)) ]
            points += word.count(guess) # FIXME Don't count duplicate guesses
            print(f"Right! Score is {points}")
        else:
            points -= 1
            print(f"Sorry, guess again. Score is {points}")

def preprocess(toks: list[str]) -> tuple[list[str], list[str]]:
    sws = stopwords.words("english")

    toks = map(lambda t: t.lower(), toks)
    toks = filter(lambda t: t.isalpha() and t not in sws and len(t) > 5, toks)
    toks = list(toks)

    wnl = WordNetLemmatizer()
    lemmas = map(lambda t: wnl.lemmatize(t), toks)
    lemmas = set(lemmas)

    nouns = filter(lambda l: l[1].startswith("N"), nltk.pos_tag(lemmas))
    nouns = map(lambda n: n[0], nouns)
    nouns = list(nouns)

    print(f"{len(toks)} tokens, {len(nouns)} nouns")
    
    return (toks, nouns)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("The only argument must be a path to the data", file=sys.stderr)
        sys.exit(1)

    for package in PACKAGES:
        nltk.download(package, download_dir="./.venv/nltk_data/", quiet=True)

    try:
        with open(sys.argv[1]) as file:
            data = file.read()
    except OSError as err:
        print(f"Cannot read file: {err.strerror}", file=sys.stderr)
        sys.exit(1)

    toks = nltk.word_tokenize(data)
    (toks, nouns) = preprocess(toks)

    # Dicts preserve insertion order as of Python 3.7
    # https://docs.python.org/3/whatsnew/3.7.html
    counts = dict(sorted(
        map(lambda n: (n, toks.count(n)), nouns), key=operator.itemgetter(1)))

    top50: list[str] = []
    for word, count in list(counts.items())[-50:]:
        top50.append(word)
        print(f"{word}: {count}")

    guessing_game(top50)

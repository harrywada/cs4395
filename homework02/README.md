# Homework 02: Word guess game

A small hangman-esque game and exercise in [NLTK](https://www.nltk.org/)
processing. Given a corpus (provided is `anat19.txt`, an excerpt from an
anatomy textbook), the script prints the number of tokens, the number of unique
nouns, and the fifty most popular of these nouns.

Subsequently, a random word will be chosen of these and the player will be
prompted to guess letters until the complete word is revealed (or the player
runs out of points). Beginning with five points, the word will be presented to
the user initially only as a series of underscores, which will be populated
with the corresponding letter as the player makes correct guesses. Failed
guesses deduct a point from the player's score, while correct guesses increment
the score by the number of revealed letters. Once the player has revealed all
letters, the script chooses a new word and the game repeats, with the score
from the previous game being carried over to the new one.

## Setup

Since this is only an exercise, the script is rather opinionated on how it
wants to be set up. Since type hints like `dict` and `list` are used, it is
necessary to use at least Python 3.9. Additionally, the script requires data
packages from NLTK, and it expects these in specific locations.

One of the best ways to isolate the Python environment is to create a virtual
environment. The commands below will create this environment in a `.venv`
directory, and then immediately enter into it.

```sh
python3 -m venv .venv
source .venv/bin/activate
```

Once this is done, you can install the dependencies without affecting your
system Python installation.

```sh
pip3 install -r requirements.txt
```

These steps must be followed for the script to work, since it will attempt to
store the downloaded NLTK data in the virtual Python environment under `.venv`.

To restore the shell to using the system-wide Python installation, do:

```sh
deactivate
```

## Usage

There must be only a single argument to the script—the path to a text file
containing the corpus to be processed. For the provided data set, this will
looking something like:

```sh
python3 main.py anat19.txt
```
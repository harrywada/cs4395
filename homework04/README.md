# Homework 04: Ngrams

A small set of programs that take use a corpus to test the similarity of novel
input (some example data is contained in `data.zip`).

## Usage

The first program `prog1.py` generates pickle files containing unigrams and
bigrams for the corpus data; to use it simply run

```sh
# You can pass multiple paths and pickle files will be generated for each
python3 prog1.py /path/to/corpus...
```

The pickle files will be generated in the same directory as the corpus.

Then, to compare to novel input, pass the second program an input file (for
interactive input you can use `/dev/stdin`) and then the "stem" for the pickle
files. This is the part of the path before `_{unigrams,bigrams}.pickle`. So a
typical invocation might look like

```sh
# Similar to prog1.py, multiple stems can be passed at once
python3 prog2.py /path/to/input stems...
```

## Installation

The programs require minimal dependencies, except for NLTK and a few of its
packages. It is expected that you are using these inside of a virtual Python
environment located at `.venv`. This can be created like so

```sh
python3 -m venv .venv
```

Additionally, since type hints are used, at least Python 3.11 is required.
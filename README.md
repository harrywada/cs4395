# CS 4395

A temporary repository containing all homework assignments for _CS 4395: Human
Language Technologies_.

## Homework 00: An Overview of NLP

The first homework assignment consists of creating this repository along with a
short list of introductory questions to answer. This has been accomplished via
my favorite general-purpose markup language: (g)roff. While a
[Makefile](./homework00/Makefile) has been included to build the resultant PDF
file, I've also included [the file itself](./homework00/homework00.pdf) for
convenience.

## Homework 01: Text processing with Python

A short little demo assignment that manually reads a CSV file, parses it into
instances of a `Person` class (along with allowing the user to interactively
fix any malformed data), and does a funny little dance of writing and
immediately reading it back from a temporary pickle file before printing the
entries out in a human-readable format.

For more information, check the [README](./homework01/README.md).

## Homework 02: Word guess game

A brief "game" and exercise in basic NLTK operations. Given a text file, the
script processes it (tokenization, lemmatization, etc.), outputs some basic
statistics, and then uses the set of nouns as input to an interactive
hangman-style game.

See the [README](./homework02/README.md) for additional documentation.

## Homework 03: WordNet

This assignment provides an introduction to the NLTK wrapper to WordNet, along
with some basic instructional tasks in lemma relationships, hierarchies, and
sentiment analysis. There is a brief section at the end dealing with
collocations and calculating the point-wise mutual information value of one
from a corpus. The report itself can be found
[here](./homework03/homework03.pdf).

## Homework 04: N-grams

This assignment once again uses NLTK to generate unigram and bigram indexes
from a corpus and use them to build probabilistic language models to evaluate
novel input. An adjunct [report](./homework04/homework04.pdf) is provided as
well. For the programs themselves, see the [README](./homework04/README.md).

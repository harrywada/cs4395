# Homework 01: Text processing with Python

This is a simple demo script that, given a path to a CSV file of the form

```
first name,last name,middle initial,id,phone number
```

parses it, creates corresponding `Person` instances in an ID-keyed dictionary,
temporarily persists it in a pickle file, then reads it back and displays all
the `Person`s in a human-readable form.

## Usage

The script takes exactly one argument—the path to a CSV file to parse. This
will presumably be the provided data file, `./data/data.csv`, which contains a
few deliberate errors that will demonstrate the script's interactive
rectification capabilities. To run it in this way, simply do:

```sh
python3 main.py data/data.csv
```

## Strengths/weakness of Python text processing

While it's probably possible to write more performant code than I have here,
Python on the outset seems to me very inelegant and inefficient at common text
handling. Frequently entire lines are read into memory without knowledge of
just how big these lines actually are ahead of time, which while not unique to
Python always struck me as rather reckless. At the same time there are a decent
number of helper methods that provide a lot of convenient functionality and
reduce the amount of code that needs to be written, so overall it's not too
bad.

## What I learned

My Python knowledge could probably be classified as intermediate, so there
wasn't that much about this introductory assignment that challenged me. It's
been a couple years since I've used it so I had to briefly review some
syntaxes, and I learned a couple small tricks (e.g. the `re.VERBOSE` flag) that
I wasn't aware of before, but on the whole the process was mostly painless.

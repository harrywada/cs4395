# Homework 06: Web crawler

Shallowly crawls from an initial page and prints out key terms from each
anchored page.

## Usage

The script takes only a single optional argument, by which a user can provide
a starting URL to crawl from. Otherwise, it will use the hardcoded default.

```sh
python3 main.py [url]
```

It will then print all URLs it was successfully able to crawl to standard
output, (and log any errors for those it was unable to), store their contents
and raw data in a `pages` directory, and use tf-idf scores to determine the
most relevant terms from each page, which it will also print to standard output
in the following form:

```
/path/to/raw/data: terms...
```
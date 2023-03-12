from bs4 import BeautifulSoup
import hashlib
import logging
import math
import os
import re
from threading import Thread
from typing import Generator, Optional
from urllib import request
from urllib.error import HTTPError
from urllib.parse import urlparse
import sys

DATA_DIR = "./pages/"
DEFAULT_URL = "https://en.wikipedia.org/wiki/Bob_Dylan"

def crawl(url: str) -> Generator[str, None, None]:
    """Generate all the URLs from anchors in an initial URL."""
    logging.info(f"Fetching initial {url}")
    data = request.urlopen(url).read().decode("utf8")
    soup = BeautifulSoup(data, features="html.parser")
    # Better to go one anchor at a time than use find_all.
    a = soup.find("a")
    while a is not None:
        href = a.get("href")
        if href is not None:
            logging.info(f"Yielding {href}")
            yield href
        a = a.find_next("a")

    logging.info("Done crawling")


def save(url: str, directory=DATA_DIR) -> Optional[str]:
    """Persist HTML with filename based on the MD5 hash of the data."""
    logging.info(f"Fetching {url}")
    try:
        html = request.urlopen(url).read().decode("utf8")
    except HTTPError as e:
        logging.error(f"GET {url} failed with code {e.code}: {e.reason}")
        return None
    except:
        logging.error(f"Failed to fetch {url}")
        return None

    h = hashlib.new("md5")
    h.update(html.encode())
    path = f"{directory}/{h.hexdigest()}.html"
    if os.path.isfile(path):
        logging.warning(f"{path} already exists for {url}; skipping")
        return

    with open(path, "w") as f:
        f.write(html)

    logging.info(f"Saved {url} to {path}")
    return path


def scrub(path: str) -> str:
    """Filter all but paragraph text from a locally stored HTML file."""
    logging.info(f"Scrubbing {path}")
    with open(path) as f:
        data = f.read()
        soup = BeautifulSoup(data, features="html.parser")

    stub = re.sub(".html?$", "", path)
    scrub_path = f"{stub}_raw.txt"
    logging.info(f"Writing processed data of {path} to {scrub_path}")
    with open(scrub_path, "w") as f:
        raw = " ".join(map(lambda t: t.get_text(), soup.find_all("p")))
        raw = re.sub("\s+", " ", raw.strip())
        f.write(raw)

    logging.info(f"Done scrubbing {path} to {scrub_path}")
    return scrub_path


def tfidf(paths: list[str]) -> dict[str, list[str]]:
    """Calculate the tf-idf scores of all terms from a list of local paths."""
    logging.info("Calculating tf-idf scores")

    def tf(toks: list[str]) -> dict[str, int]:
        tf_data: dict[str, int] = {}
        for t in toks:
            tf_data[t] = tf_data[t] + 1 if t in tf_data else 1

        for t in tf_data.keys():
            tf_data[t] = tf_data[t] / len(toks)

        return tf_data

    def idf(corpora: list[list[str]]) -> dict[str, int]:
        assert len(corpora) == len(paths) # Sanity check.

        idf_data: dict[str, int] = {}
        vocab: list[str] = []
        for c in corpora:
            for i in c:
                if i not in vocab:
                    vocab.append(i)

        for v in vocab:
            n = len(list(filter(lambda c: v in c, corpora)))
            idf_data[v] = math.log((1 + n) / len(corpora))

        return idf_data

    corpora: dict[str, list[str]] = {}
    tf_vals: list[dict[str, int]] = []
    for p in paths:
        with open(p) as f:
            data = f.read()

        re.sub("[`~!@#$%^&*()-_=+[{\]}\\|]", "", data)
        toks = data.split()
        toks = list(filter(lambda t: t.isalpha(), toks))
        corpora[p] = toks

        tf_vals.append(tf(toks))

    idf_vals = idf(corpora.values())

    tfidf_vals: dict[str, dict[str, int]] = {}
    # Take advantage of the fact that as of Python 3.7+ dicts are ordered.
    assert len(tf_vals) == len(paths)
    for i in range(len(tf_vals)):
        for t, tfv in tf_vals[i].items():
            if paths[i] not in tfidf_vals:
                tfidf_vals[paths[i]] = {}
            # XXX Some very messy indexing here.
            tfidf_vals[paths[i]][t] = tfv * idf_vals[t]

    logging.info("Done calculating tf-idf scores")
    return tfidf_vals


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    threads: list[Thread] = []

    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Each of the URLs will be passed to this in their own thread.
    def handle(u: str) -> None:
        path = save(u)
        if path != None:
            scrub(path)

    for u in crawl(url):
        if u.startswith("#"):
            continue
        if u.startswith("/"):
            u = urlparse(url).netloc + u
        if not u.startswith("http"):
            u = "http://" + u

        print(u)
        threads.append(Thread(target=handle, args=(u,)))
        threads[-1].start()

    for t in threads:
        t.join()
    logging.info("Done extracting data")

    corpora = [ os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR)
                                     if f.endswith("_raw.txt")     ]
    for path, scores in tfidf(corpora).items():
        top25 = sorted(scores.keys(), key=lambda k: scores[k])[:25]
        print(f"{path}: {', '.join(top25)}")

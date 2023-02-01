from typing import Dict, TextIO
import logging
import os
import pickle
import re
import sys
import tempfile

class Person:
    """A person as described by their first and last name, middle initial, ID,
    and phone number.
    """

    # The ID_PATTERN is a little ugly since the sample run seems to indicate
    # that phone number separators (if they exist) must match, and it's invalid
    # if they don't. Since regex are only state machines, there's no good way
    # of verifying this without hard-coding possible separators (i.e. the dot,
    # slash, and space), which is still much uglier than if the constraints
    # were only a bit more rigid.
    ID_PATTERN = re.compile("[A-Z]{2}[0-9]{4}")
    PN_PATTERN = re.compile("""
        [0-9]{3}
        (
               -?[0-9]{3}-?[0-9]{4}  # Dash separator
            | \.?[0-9]{3}\.?[0-9]{4} # Period separator
            | \ ?[0-9]{3}\ ?[0-9]{4} # Space separator
        )
    """, re.VERBOSE)

    def display(self) -> None:
        print(self)

    def __init__(self, lname: str, fname: str, mi: str, id: str, pn: str) -> None:
        if len(mi) != 1:
            raise ValueError("The middle initial must be a single letter")
        elif not self.ID_PATTERN.match(id):
            raise ValueError("The ID must comprise of two uppercase letters followed by four digits")
        elif not self.PN_PATTERN.match(pn):
            raise ValueError("The phone number must comprise of ten digits")

        self.lname = lname
        self.fname = fname
        self.mi = mi
        self.id = id
        self.pn = pn

    def __str__(self) -> str:
        return (
            f"Employee id: {self.id}\n"
            f"\t{self.fname} {self.mi} {self.lname}\n"
            f"\t{self.pn}\n"
        )


def parse_csv(fileobj: TextIO) -> Dict[str, Person]:
    persons: Dict[str, Person] = {}
    for line in fileobj:
        line = line.strip("\n")
        fields = line.split(",")
        if len(fields) != 5:
            logging.warning(f"Invalid number of fields: {line}")
            continue
        
        lname = fields[0]
        fname = fields[1]
        mi    = fields[2]
        id    = fields[3]
        pn    = fields[4]

        while not Person.ID_PATTERN.match(id):
            if not sys.stdin.isatty():
                raise ValueError(f"Failed to parse ID: {id}")

            # Don't use logging here to conform to example cases.
            print(f"ID invalid: {id}", file=sys.stderr)
            print("ID is two letters followed by 4 digits", file=sys.stderr)
            id = input("Please enter a valid id: ")

        while not Person.PN_PATTERN.match(pn):
            if not sys.stdin.isatty():
                raise ValueError(f"Failed to parse phone number: {pn}")

            # Again, don't log for conformity to example cases.
            print(f"Phone {pn} is invalid", file=sys.stderr)
            print("Enter phone number in form 123-456-7890", file=sys.stderr)
            pn = input("Enter phone number: ")

        if id in persons:
            logging.error(f"Duplicate id: {id}")
            continue

        persons[id] = Person(
            lname.title(),
            fname.title(),
            mi.upper() if len(mi) else "X",
            id,
            pn,
        )

    return persons


if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error(f"Usage: {sys.argv[0]} path...")
        sys.exit(1)

    try:
        with open(sys.argv[1]) as f:
            f.readline() # Ignore the first header line
            persons = parse_csv(f)
    except OSError as e:
        logging.error(f"Failed to open {sys.argv[1]}: {e}")
        sys.exit(1)

    # In order to minimize likelihood of file collision, create the pickle file
    # under the OS-specific temporary directory with the name <PID>.tmp.
    tmpdir = tempfile.gettempdir()
    pid = os.getpid()
    pickle_path = os.path.join(tmpdir, f"{pid}.tmp")
    with open(pickle_path, "wb") as f:
        pickle.dump(persons, f)

    # Since it's unlikely (although possible) that the pickle file has
    # disappeared since we saved it, it's reasonable to assume it exists and
    # not use a try/except as was used for sys.argv[1].
    with open(pickle_path, "rb") as f:
        persons = pickle.load(f)

    os.remove(pickle_path)

    print("Employee list:\n")
    for p in persons:
        persons[p].display()

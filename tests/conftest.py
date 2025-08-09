import json
import pathlib
from collections.abc import Iterable
from types import SimpleNamespace

import pytest

# Pytest suggests defining all fixtures within a single conftest.py file:
#   gist.github.com/peterhurford/09f7dcda0ab04b95c026c60fa49c2a68


@pytest.fixture
def unicode_stripped_pairs() -> Iterable[tuple[str, str]]:
    def genpairs() -> Iterable[tuple[str, str]]:
        yield "ş", "s"
        yield (
            "kaderdenkesişenyollarinhikayesi.xyz",
            "kaderdenkesisenyollarinhikayesi.xyz",
        )  # , 35
        yield "şéàşöñ", "season"  # , 6
        yield "ç", "c"
        yield "かな漢字", "かな漢字"  # These are identical

    yield genpairs()


def _parse_hex(x: str | list) -> int | list[int]:
    # Case 1: we have been given a hex value directly
    if isinstance(x, str):
        # Type remark: this is unsafe in a sense as we assume that the string
        # given is parseable into a hex integer!  E.g., looks like 0x...  This
        # should be true for all test data.
        return int(x, 16)

    # Case 2: we need to parse
    if isinstance(x, list):
        return [_parse_hex(e) for e in x]

    # Case 3: I don't know what to do with this!
    raise TypeError(f"Cannot parse hex from {type(x).__name__!r}")


def _tupleify(x: list[int | list[int]]) -> list[int | tuple[int, int]]:
    # Type remark: we assume this input is a list.  This should be true for all
    # test data.

    # Case 1: the provided list is not nested; return the input unchanged.
    #
    # See also `eltype` implementation:
    #   github.com/jakewilliami/places-of-worship/
    #     blob/2496ff0f/src/powdb/common/utils/eltype.py
    if all(not isinstance(e, list) for e in x):
        return x

    # Case 2: Now we must have that at least some of the elements of `x` are
    # lists.  These lists are the JSON-representation of tuples, so we should
    # tuple-ify them here.
    #
    # Note that we assume that *all* elements of `x` are lists and of the same
    # type.  We also assume that they are of length 2.  This should be true
    # for all test data.
    return [tuple(e) for e in x]


def _load_data(f: str) -> list[int | tuple[int, int]]:
    # Step 1: load the JSON
    data = json.loads(f.read_text())

    # Step 2: convert all strings into hex
    data = _parse_hex(data)

    # Step 3: if given nested lists, make inner lists into tuples
    data = _tupleify(data)

    return data


@pytest.fixture(scope="session")
def data():
    # Specify the data directory
    data_dir = pathlib.Path(__file__).parent / "data"

    # Iterate over data directory and construct a namespace for all data
    data = {}
    for f in data_dir.iterdir():
        # We only want to deal with JSON data files
        if not (f.is_file() and f.suffix == ".json"):
            continue

        data[f.stem] = _load_data(f)

    return SimpleNamespace(**data)

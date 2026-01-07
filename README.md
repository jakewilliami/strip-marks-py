# `strip_marks`

A small Python library for stripping non-spacing marks (e.g., diacritics; accents) from a string.

---

## Quick Start

```python
from strip_marks import strip_marks

assert strip_marks("şéàşöñ") == "season"
assert strip_marks("kaderdenkesişenyollarinhikayesi.xyz") == "kaderdenkesisenyollarinhikayesi.xyz"

def identity(x): return x
assert strip_marks("hello world") == identity("hello world")
```

## Using `strip_marks` as a Library

This package is published on PyPI.  You can install it with PIP:

```commandline
$ pip add strip-marks
```

Or, if using [UV](https://github.com/astral-sh/uv/) for dependency management:

```commandline
$ uv add strip-marks
```

## Notes on Internal Functionality

This library uses [Python's `unicodedata` standard library](https://docs.python.org/3/library/unicodedata.html) for normalising strings to strip marks.

Early (incomplete) versions of the library implemented (and used internally) functions adapted from the [`utf8proc` C library](https://github.com/JuliaStrings/utf8proc) to handle characters of multiple codepoints.  This implementation used bitwise functionality from our sister package, [`ispunct`](https://github.com/jakewilliami/ispunct-py).  I would like to continue to explore this lower-level problem space to see if I can implement something in Python that is more efficient than the [current implementation](https://github.com/jakewilliami/strip-marks-py/tree/v1.0.0).

## Alternative Libraries

This was written mostly as a proof of concept.  A more developed library with this functionality is [`unidecode`](https://pypi.org/project/Unidecode/).  A curious reader may also be interested in [`unihandecode`/`pykakasi`](https://pypi.org/project/pykakasi/) or [`text-unidecode`](https://pypi.org/project/text-unidecode/).

## Citation

If your research depends on `strip_marks`, please consider giving us a formal citation: [`citation.bib`](./citation.bib).

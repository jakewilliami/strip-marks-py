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

This package is not published on PyPI, but you can use it from Git.  For example, if using [UV](https://github.com/astral-sh/uv/) for dependency management, you could write:

```shell
$ uv add "strip_marks @ git+https://github.com/jakewilliami/strip-marks-py"
```

## Notes on Internal Functionality

This library also implements (and uses internally) functions adapted from the `utf8proc` C library to handle characters of multiple codepoints.  We also use bitwise functionality from our sister package, [`ispunct`](https://github.com/jakewilliami/ispunct-py).

## Alternative Libraries

This was written mostly as a proof of concept.  A more developed library with this functionality is [`unidecode`](https://pypi.org/project/Unidecode/).  A curious reader may also be interested in [`unihandecode`/`pykakasi`](https://pypi.org/project/pykakasi/) or [`text-unidecode`](https://pypi.org/project/text-unidecode/).

## Citation

If your research depends on `strip_marks`, please consider giving us a formal citation: [`citation.bib`](./citation.bib).

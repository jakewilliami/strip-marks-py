from typing import Iterable

import pytest

import strip_marks


@pytest.fixture
def unicode_stripped_pairs() -> Iterable[tuple[str, str]]:
    def genpairs() -> Iterable[tuple[str, str]]:
        yield "kaderdenkesişenyollarinhikayesi.xyz", "kaderdenkesisenyollarinhikayesi.xyz"
        yield "şéàşöñ", "season"
        yield "かな漢字", "かな漢字"  # These are identical

    yield from genpairs()


def test_strip_marks(unicode_stripped_pairs: Iterable[tuple[str, str]]):
    for (s1, s2) in unicode_stripped_pairs:
        assert strip_marks.strip_marks(s1) == s2

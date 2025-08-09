from collections.abc import Iterable

import strip_marks


def test_strip_marks(unicode_stripped_pairs: Iterable[tuple[str, str]]):
    for s1, s2 in unicode_stripped_pairs:
        assert strip_marks.strip_marks(s1) == s2


def test_strip_chars_changes(data):
    for a, b in data.changes:
        s1, s2 = chr(a), chr(b)
        expected = strip_marks.strip_marks(s1)
        assert expected == s2
        assert ord(expected) == b


def test_strip_chars_no_changes(data):
    for x in data.no_changes:
        s = chr(x)
        expected = strip_marks.strip_marks(s)
        assert expected == s
        assert ord(expected) == x


def test_strip_chars_spaces(data):
    for x in data.spaces:
        s = chr(x)
        expected = strip_marks.strip_marks(s)
        assert expected == s
        assert ord(expected) == x


def test_strip_chars_unusual(data):
    for x in data.unusual:
        s = chr(x)
        expected = strip_marks.strip_marks(s)
        assert expected == s
        assert ord(expected) == x

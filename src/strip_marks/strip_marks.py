import unicodedata

from strip_marks.unicode import utf8proc_map
from strip_marks.unicode.constants import UTF8PROC_COMPOSE, UTF8PROC_STRIPMARK


def strip_marks(s: str) -> str:
    """
    Strip non-spacing marks (e.g., accents) from input string.

    Adapted from a specialised usecase of Julia's `normalize` function:
      <https://github.com/JuliaLang/julia/blob/17fff87/base/strings/unicode.jl#L197-L236>
    """
    if all(unicodedata.combining(c) for c in s):
        return s

    return utf8proc_map(s, UTF8PROC_COMPOSE | UTF8PROC_STRIPMARK)

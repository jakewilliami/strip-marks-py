from strip_marks.constants import UTF8PROC_COMPOSE, UTF8PROC_STRIPMARK
from strip_marks.unicode import utf8proc_map


def strip_marks(s: str) -> str:
    """
    Strip non-spacing marks (e.g., accents) from input string.

    Adapted from a specialised usecase of Julia's `normalize` function:
      <https://github.com/JuliaLang/julia/blob/17fff87/base/strings/unicode.jl#L197-L236>
    """
    return utf8proc_map(s, UTF8PROC_COMPOSE | UTF8PROC_STRIPMARK)

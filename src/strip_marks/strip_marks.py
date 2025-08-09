import unicodedata


def strip_marks(s: str) -> str:
    """
    Strip non-spacing marks (e.g., accents) from input string.
    """

    # Base case: return input string is only made up of combining characters
    if all(unicodedata.combining(c) for c in s):
        return s

    # Step 1: decompose input into normal form
    s_norm = unicodedata.normalize("NFD", s)

    # Step 2: keep only base characters
    s_base = ''.join(ch for ch in s_norm if not unicodedata.combining(ch))

    # Step 3: re-compose normalised form without base characters
    return unicodedata.normalize("NFC", s_base)

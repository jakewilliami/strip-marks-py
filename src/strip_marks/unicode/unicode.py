from functools import lru_cache
import unicodedata

from strip_marks.unicode.constants import *


@lru_cache(maxsize=1)
def _composition_map() -> dict[tuple[int, int], int]:
    """
    Inverse of the canonical decomposition mapping, building a reverse index
    instead of a per-codepoint flag.
    """
    composition = {}

    # Build a complete composition mapping for all valid character values.
    # Unicode scalar values are 0–0xD7FF and 0xE000–0x10FFFF.
    #
    # Values stolen from Julia's `rand(::Char)` function:
    #   <github.com/JuliaLang/julia/blob/7fa26f01/stdlib/Random/src/generation.jl#L164-L168>
    for cp in (cp if cp < 0xD800 else cp + 0x800 for cp in range(0x10f800)):
        decomp = unicodedata.decomposition(chr(cp))
        if not decomp or decomp.startswith("<"):
            continue

        parts = [int(p, 16) for p in decomp.split()]
        if len(parts) != 2:
            continue

        first, second = parts
        if unicodedata.combining(chr(first)) != 0:
            continue  # first component must be a starter

        composition[(first, second)] = cp

    return composition


@lru_cache(maxsize=None)
def is_canonical_decomposition(cp: int) -> bool:
    """
    We check if a codepoint is a *canonical* decomposition.  This works because
    the UnicodeData.txt table defines a mapping field as
        <decomposition type> decomposition mapping
    Or simply
        decomposition mapping
    for canonical decompositions

    Ref:
      <https://www.unicode.org/Public/17.0.0/ucd/UnicodeData.txt>

    I still wish we could do this more elegantly, such as using a simple
    `property->decom_type` field as `utf8proc` does.
    """
    if not (decomp := unicodedata.decomposition(chr(cp))):
        return False

    first_token, _, _ = decomp.partition(" ")
    return not (first_token.startswith("<") and first_token.endswith(">"))


def utf8proc_decompose_char(cp: int, options: int) -> list[int]:
    """
    Decomposes a UTF-8 codepoint with specified flags controlling normalisation
    behaviour.

    We currently only support normalisation for stripping non-spacing marks from
    the character, with no custom mapping.

    Modifies the given buffer and returns the resulting size of the decomposed
    character array.

    Adapted from the utf8proc library code for the same function:
      <https://github.com/JuliaStrings/utf8proc/blob/a1b99da/utf8proc.c#L452-L538>

    The primary difference here is that we return the full buffer in the first
    pass, rather than passing the buffer to the function and filling it
    iteratively.
    """
    if options != (UTF8PROC_COMPOSE | UTF8PROC_STRIPMARK):
        raise ValueError(f"A generalised form of this function is not yet supported")

    # Check that code point is a valid Unicode scalar value
    #
    # Values stolen from Julia's `rand(::Char)` function:
    #   <github.com/JuliaLang/julia/blob/7fa26f01/stdlib/Random/src/generation.jl#L164-L168>
    if not (0 <= cp <= 0x10FFFF) or 0xD800 <= cp <= 0xDFFF:
        raise ValueError("Character not assigned in Unicode")

    hangul_sindex = cp - UTF8PROC_HANGUL_SBASE

    if 0 <= hangul_sindex < UTF8PROC_HANGUL_SCOUNT:
        l = UTF8PROC_HANGUL_LBASE + hangul_sindex // UTF8PROC_HANGUL_NCOUNT
        v = UTF8PROC_HANGUL_VBASE + (hangul_sindex % UTF8PROC_HANGUL_NCOUNT) \
            // UTF8PROC_HANGUL_TCOUNT
        hangul_tindex = hangul_sindex % UTF8PROC_HANGUL_TCOUNT

        if hangul_tindex == 0:
            return [l, v]

        return [l, v, UTF8PROC_HANGUL_TBASE + hangul_tindex]

    ch = chr(cp)

    if is_canonical_decomposition(cp):
        out = []
        for part in unicodedata.decomposition(ch).split():
            out.extend(utf8proc_decompose_char(int(part, 16), options))

        return out

    return [cp]


def utf8proc_decompose(s: list[int], options: int) -> list[int]:
    """
    Decompose a UTF-8 string with specified flags controlling normalisation
    behaviour.

    We currently only support normalisation for stripping non-spacing marks from
    strings, with no custom mapping.

    Adapted from the utf8proc library code for the same function:
      <https://github.com/JuliaStrings/utf8proc/blob/a1b99da/utf8proc.c#L547-L612>

    The primary difference here is that we return the full buffer in the first
    pass, rather than passing the buffer to the function and filling it
    iteratively.
    """
    if options != (UTF8PROC_COMPOSE | UTF8PROC_STRIPMARK):
        raise ValueError("A generalised form of this function is not yet supported")

    buf = []
    for cp in s:
        # Code points may canonically decompose into other code points.  We can
        # call these `b` for lack of a better term.  They may be bytes if UTF-8
        # or pairs of bytes in UTF-16; not entirely sure what to call them.
        # `b` refers to the "bits" that the code point decomposes to, but not
        # computer bits!  Just "bits" from English.  Pieces of the code point.
        for b in utf8proc_decompose_char(cp, options):
            # Only keep "bits" that are not combining marks.
            #
            # Ref:
            #   <https://www.unicode.org/reports/tr44/tr44-34.html#Canonical_Combining_Class_Values>
            if unicodedata.combining(chr(b)) == 0:
                buf.append(b)

    # Sort by combining class
    # TODO: do we need this?  Every character should have combining class 0
    # Maybe we need to sort s before decomposing?
    buf.sort(key=lambda c: unicodedata.combining(chr(c)))
    return buf


def utf8proc_reencode(cps: list[int], options: int) -> list[int]:
    """
    Recompose codepoints from decomposed form.

    Adapted from the utf8proc library code for the same function:
      <https://github.com/JuliaStrings/utf8proc/blob/a1b99da/utf8proc.c#L730-L752>
    """
    if options & ~(UTF8PROC_COMPOSE | UTF8PROC_STRIPMARK):
        raise ValueError("A generalised form of this function is not yet supported")

    if not (options & UTF8PROC_COMPOSE):
        return cps

    composition = _composition_map()
    buf, i, n = [], 0, len(cps)

    while i < n:
        cp = cps[i]

        # Similar to `utf8proc_decompose_char`, we have to provide special
        # handling for Hangul characters, because unlike non-Hangul characters
        # (which much contain at least one combining mark, which
        # UTF8PROC_STRIPMARK removed before recomposition can occur), Hangul
        # character components all have combining class of 0 and therefore
        # survive stripping (by design).
        l_index = cp - UTF8PROC_HANGUL_LBASE

        if 0 <= l_index < UTF8PROC_HANGUL_LCOUNT and i + 1 < n:
            v_index = cps[i + 1] - UTF8PROC_HANGUL_VBASE

            if 0 <= v_index < UTF8PROC_HANGUL_VCOUNT:
                t_index, consumed = 0, 2

                if i + 2 < n:
                    cand_t = cps[i + 2] - UTF8PROC_HANGUL_TBASE

                    if 0 < cand_t < UTF8PROC_HANGUL_TCOUNT:
                        t_index, consumed = cand_t, 3

                syllable = (
                    UTF8PROC_HANGUL_SBASE
                    + (l_index * UTF8PROC_HANGUL_VCOUNT + v_index)
                    * UTF8PROC_HANGUL_TCOUNT
                    + t_index
                )

                buf.append(syllable)
                i += consumed
                continue

        # Add the final stripped codepoints to the output buffer
        cp1 = cp
        j = i + 1
        while j < n and (cp1, cps[j]) in composition:
            cp1 = composition[(cp1, cps[j])]
            j += 1

        buf.append(cp1)
        i = j

    return buf


def codepoints(s: str) -> list[int]:
    """
    Convert a Unicode string into Unicode code point integers.
    """
    # TODO: is `list(map(ord, s))` faster?
    return [ord(c) for c in s]


def utf8proc_map(s: str, options: int):
    """
    Calculate required buffer size and apply decomposition for the given UTF-8
    string.

    Adapted from Julia's function of the same name:
      <https://github.com/JuliaLang/julia/blob/17fff87/base/strings/unicode.jl#L168-L175>
    """
    # TODO: can we do this?
    # import array
    # decomposed = utf8proc_decompose(cps, options)
    # recomposed = utf8proc_decompose(decomposed, options)
    # return array.array('I', recomposed).tobytes().decode('utf-32-le')
    # decode would break if input is a lone surrogate, but that shouldn't happen?
    cps = codepoints(s)
    decomposed = utf8proc_decompose(cps, options)
    recomposed = utf8proc_reencode(decomposed, options)
    return "".join(chr(cp) for cp in recomposed)


# UTF8 processing options
#   <https://github.com/JuliaStrings/utf8proc/blob/20d192ac/utf8proc.h#L154>
#   <https://github.com/JuliaStrings/utf8proc/blob/a1b99da/utf8proc.h#L207>
UTF8PROC_COMPOSE = 1 << 3
UTF8PROC_STRIPMARK = 1 << 13

# Hangul constants
#   <https://github.com/JuliaStrings/utf8proc/blob/a1b99da/utf8proc.c#L74-L92>
UTF8PROC_HANGUL_SBASE = 0xAC00
UTF8PROC_HANGUL_LBASE = 0x1100
UTF8PROC_HANGUL_VBASE = 0x1161
UTF8PROC_HANGUL_TBASE = 0x11A7
UTF8PROC_HANGUL_LCOUNT = 19
UTF8PROC_HANGUL_VCOUNT = 21
UTF8PROC_HANGUL_TCOUNT = 28
UTF8PROC_HANGUL_NCOUNT = 588
UTF8PROC_HANGUL_SCOUNT = 11172

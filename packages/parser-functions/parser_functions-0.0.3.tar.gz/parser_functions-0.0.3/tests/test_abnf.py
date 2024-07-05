# from pprint import pprint

# import pytest

# from parser_functions.abnf import ABNF, CodeGen
# from parser_functions.combinators import Stream

# CSV_ABNF = """
# ; pre name
# name = field ;name
# ; after name

# header = name *(COMMA name)

# record = field *(COMMA field)

# field = (escaped / non-escaped)

# non-escaped = *TEXTDATA

# file = [header CRLF] record *(CRLF record) [CRLF]

# escaped = DQUOTE *(TEXTDATA / COMMA / CR / LF / 2DQUOTE) DQUOTE

# COMMA = %x2C

# CR = %x0D ;as per section 6.1 of RFC 2234 [2]

# DQUOTE = %x22 ;as per section 6.1 of RFC 2234 [2]

# LF = %x0A ;as per section 6.1 of RFC 2234 [2]

# CRLF = CR LF ;as per section 6.1 of RFC 2234 [2]

# TEXTDATA =  %x20-21 / %x23-2B / %x2D-7E
# """


# def test_csv_abnf():
#     abnf = ABNF()
#     r = next(abnf.rulelist(Stream.from_string(CSV_ABNF)))
#     # pprint(r.value, width=80)
#     gen = CodeGen()
#     gen.generate(r.value)

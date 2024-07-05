import re
import string

from parser_functions.combinators import Combinators, Stream
from tests.helpers import assert_fail, assert_success

c = Combinators()


class TestCombinators:
    def test_shift(self):
        assert_success(
            next(c.shift(Stream.from_string("test"))),
            "t",
            1,
        )

    def test_nothing(self):
        assert_success(
            next(c.nothing(Stream.from_string("test"))),
            None,
            0,
        )

    def test_filter(self):
        assert_success(
            next(c.filter(lambda c: c == "t")(c.shift)(Stream.from_string("test"))),
            "t",
            1,
        )
        assert_fail(
            next(c.filter(lambda c: c == "t")(c.shift)(Stream.from_string("sample"))),
        )

    def test_literal(self):
        assert_success(
            next(c.literal("t")(c.shift)(Stream.from_string("test"))), "t", 1
        )

    def test_char(self):
        assert_success(
            next(c.char("t")(Stream.from_string("test"))),
            "t",
            1,
        )
        assert_fail(
            next(c.char("t")(Stream.from_string("sample"))),
        )

    def test_word(self):
        assert_success(next(c.word('bus')(Stream.from_string('bus'))), "bus", 3)
        assert_success(next(c.word('bus')(Stream.from_string('bust'))), "bus", 3)

    def test_regex(self):
        regex = re.compile("[abc]")
        assert_success(next(c.regex(regex)(Stream.from_string("abcd"))), "a", 1)
        assert_success(next(c.regex(regex)(Stream.from_string("bcde"))), "b", 1)
        assert_success(next(c.regex(regex)(Stream.from_string("cdef"))), "c", 1)
        assert_fail(
            next(c.regex(regex)(Stream.from_string("defg"))),
        )

    def test_all_except(self):
        not_abc = c.all_except(["a", "b", "c"])
        for char in [letter for letter in string.printable if letter not in "abc"]:
            assert_success(next(not_abc(Stream.from_string(char))), char, 1)
        assert_fail(
            next(not_abc(Stream.from_string("a"))),
        )
        assert_fail(
            next(not_abc(Stream.from_string("b"))),
        )
        assert_fail(
            next(not_abc(Stream.from_string("c"))),
        )

    def test_map(self):
        assert_success(
            next(c.map(str.upper)(c.char("t"))(Stream.from_string("test"))), "T", 1
        )

    def test_either(self):
        assert_success(
            next(c.either(c.char("a"), c.char("b"))(Stream.from_string("abc"))), "a", 1
        )
        assert_success(
            next(c.either(c.char("b"), c.char("a"))(Stream.from_string("abc"))), "a", 1
        )
        assert_success(
            next(c.either(c.char("a"), c.char("b"))(Stream.from_string("bcd"))), "b", 1
        )
        assert_fail(
            next(c.either(c.char("a"), c.char("b"))(Stream.from_string("cde"))),
        )

    def test_choice(self):
        options = c.choice(c.char("a"), c.char("b"), c.char("c"))
        assert_success(next(options(Stream("abc"))), "a", 1)
        assert_success(next(options(Stream("bcd"))), "b", 1)
        assert_success(next(options(Stream("cde"))), "c", 1)
        assert_fail(
            next(options(Stream("def"))),
        )

    def test_sequence(self):
        assert_success(
            next(c.sequence(c.char("a"), c.char("b"), c.char("c"))(Stream("abcd"))),
            ["a", "b", "c"],
            3,
        )
        assert_fail(
            next(c.sequence(c.char("a"), c.char("b"), c.char("c"))(Stream("abdc"))),
        )

    def test_one_or_more(self):
        a_chars = c.one_or_more(c.char("a"))
        assert [r.value for r in list(a_chars(Stream.from_string("aaaab")))] == [
            "a",
            "a",
            "a",
            "a",
        ]

    def test_zero_or_more(self):
        a_chars = c.zero_or_more(c.char("a"))
        assert [r.value for r in list(a_chars(Stream.from_string("aaaab")))] == [
            "a",
            "a",
            "a",
            "a",
        ]

        assert_success(next(a_chars(Stream.from_string("bbb"))), None, 0)

    def test_collect(self):
        a_chars = c.one_or_more(c.char("a"))
        collect = c.collect(a_chars)
        assert_success(
            next(collect(Stream.from_string("aaaab"))),
            ["a", "a", "a", "a"],
            4,
        )

    def test_repeat(self):
        assert_success(
            next(c.repeat(5)(c.digit)(Stream.from_string('12345'))),
            ['1', '2', '3', '4', '5'],
            5,
        )
        assert_fail(
            next(c.repeat(5)(c.digit)(Stream.from_string('12a45'))),
        )

    def test_letters(self):
        assert_success(next(c.letters(Stream.from_string("abc123"))), "abc", 3)

    def test_digits(self):
        assert_success(next(c.digits(Stream.from_string("123abc"))), "123", 3)

    def test_decimal_digits(self):
        assert_success(next(c.decimal_digits(Stream.from_string("10.25"))), "10.25", 5)

    def test_decimal(self):
        assert_success(next(c.decimal(Stream.from_string("10.25"))), 10.25, 5)

    def test_integer(self):
        assert_success(next(c.integer(Stream.from_string("1025"))), 1025, 4)

    def test_float(self):
        assert_success(next(c.float(Stream.from_string("1025"))), 1025, 4)
        assert_success(next(c.float(Stream.from_string("10.25"))), 10.25, 5)

    def test_whitespace(self):
        assert_success(
            next(c.whitespace(Stream.from_string("    a"))), [" ", " ", " ", " "], 4
        )

    def test_token(self):
        eq_token = c.token(c.char("="))
        assert_success(next(eq_token(Stream.from_string(" = "))), "=", 2)
        assert_success(next(eq_token(Stream.from_string("    = "))), "=", 5)

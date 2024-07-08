import pytest

from parser_functions.arithmetic import Arithmetic
from parser_functions.combinators import Stream

a = Arithmetic()


def assert_expression(expr, value):
    r = next(a.expr(Stream.from_string(expr)))
    assert r.value.evaluate() == value


@pytest.mark.parametrize(
    'expr,expected',
    [
        ('4', 4),
        ('-4', -4),
        ('0 - 4', -4),
        ('12 + 4', 16),
        ('12 - 4', 8),
        ('12 + -4', 8),
        ('12 * 4', 48),
        ('12 / 4', 3),
        ('15 % 4', 3),
        ('12 * 4 - 2', 46),
        ('12 - 4 * 2', 4),
        ('12 * (4 - 2)', 24),
        ('12 * (4 - 2)', 24),
        ('12.5 + 10', 22.5),
    ],
)
def test_arithmetic(expr, expected):
    assert_expression(expr, expected)

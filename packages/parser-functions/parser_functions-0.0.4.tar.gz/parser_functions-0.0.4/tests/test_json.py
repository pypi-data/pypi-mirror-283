import pytest

from parser_functions.json import loads


@pytest.mark.parametrize(
    'string,result',
    [
        ('"foo"', 'foo'),
        ('true', True),
        ('false', False),
        ('null', None),
        ('0', 0),
        ('1', 1),
        ('12', 12),
        ('-12', -12),
        ('2e10', 1024),
        ('1.5', 1.5),
        ('[1, 2, 3]', [1, 2, 3]),
        ('{ "key" : [ 1, 2, 3 ] }', {"key": [1, 2, 3]}),
    ],
)
def test_strict_json(string, result):
    assert loads(string, True) == result


@pytest.mark.parametrize(
    'string,result',
    [
        ('"foo"', 'foo'),
        ('true', True),
        ('false', False),
        ('null', None),
        ('0', 0),
        ('1', 1),
        ('12', 12),
        ('-12', -12),
        ('2e10', 1024),
        ('1.5', 1.5),
        ('[1, 2, 3]', [1, 2, 3]),
        ('[1, 2, 3,]', [1, 2, 3]),
        ('{ "key" : [ 1, 2, 3 ] }', {"key": [1, 2, 3]}),
        ('{ "key" : [ 1, 2, 3, ], }', {"key": [1, 2, 3]}),
        (
            (
                '// header comment \n'
                '{ "key" : // comment about the key\n'
                '[ 1, 2, 3, ],       \n'
                ' }\n // trailing comment\n'
            ),
            {"key": [1, 2, 3]},
        ),
    ],
)
def test_permissive_json(string, result):
    assert loads(string, strict=False) == result

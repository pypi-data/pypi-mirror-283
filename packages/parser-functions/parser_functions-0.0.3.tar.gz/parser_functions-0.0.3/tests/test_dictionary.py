from parser_functions.combinators import Stream
from parser_functions.dictionary import Dictionary
from tests.helpers import assert_success

d = Dictionary()


def test_dictionary():
    assert_success(
        next(
            d.dictionary(
                Stream.from_string("{k:'v', bool: TRUE, key:'value', dict: {x:12}, }")
            )
        ),
        {
            "k": "v",
            "bool": True,
            "key": "value",
            "dict": {"x": 12},
        },
        48,
    )
    assert_success(
        next(
            d.dictionary(
                Stream.from_string("{k:'v', bool: TRUE, key:'value', dict: {x:12} }")
            )
        ),
        {
            "k": "v",
            "bool": True,
            "key": "value",
            "dict": {"x": 12},
        },
        47,
    )


def test_loads():
    assert d.loads("{a: {b: {c: {}}}}") == {"a": {"b": {"c": {}}}}


def test_list():
    assert d.loads("{a: ['foo', true, 'baz', 12]}") == {"a": ["foo", True, "baz", 12]}


def test_nesting():
    assert d.loads("{key: ['inner', 12, {'nested': [1,2,3]}]}") == {
        "key": [
            'inner',
            12,
            {
                'nested': [1, 2, 3],
            },
        ]
    }

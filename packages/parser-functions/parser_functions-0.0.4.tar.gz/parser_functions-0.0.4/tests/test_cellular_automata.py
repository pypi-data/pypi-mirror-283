import pytest

from parser_functions.cellular_automata.visitors import CARuleSet


@pytest.mark.parametrize(
    'rules,method,cases',
    [
        # Game of life
        (
            '23/3',
            'does_survive',
            [
                (0, False),
                (1, False),
                (2, True),
                (3, True),
                (4, False),
                (5, False),
                (5, False),
                (7, False),
                (8, False),
            ],
        ),
        (
            '23/3',
            'is_born',
            [
                (0, False),
                (1, False),
                (2, False),
                (3, True),
                (4, False),
                (5, False),
                (5, False),
                (7, False),
                (8, False),
            ],
        ),
        (
            'B3/S23',
            'does_survive',
            [
                (0, False),
                (1, False),
                (2, True),
                (3, True),
                (4, False),
                (5, False),
                (5, False),
                (7, False),
                (8, False),
            ],
        ),
        (
            'B3/S23',
            'is_born',
            [
                (0, False),
                (1, False),
                (2, False),
                (3, True),
                (4, False),
                (5, False),
                (5, False),
                (7, False),
                (8, False),
            ],
        ),
    ],
)
def test_ca_rule_set(rules, method, cases):
    rules = CARuleSet.from_string(rules)
    method = getattr(rules, method)
    for i, test_case in enumerate(cases):
        live_neighbors, expected = test_case
        assert method(live_neighbors) == expected, f"Case {i}: {test_case}"


def test_is_born():
    rules = CARuleSet({}, {}, None)
    assert rules.is_born(1) is False


def test_does_survive():
    rules = CARuleSet({}, {}, None)
    assert rules.does_survive(1) is False

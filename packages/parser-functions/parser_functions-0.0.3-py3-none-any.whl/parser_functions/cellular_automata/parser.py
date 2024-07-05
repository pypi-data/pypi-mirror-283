"""File code generated from ABNF grammar:

rulestring = (birth-survival-notation / sb-notation) [neighborhood]  ; metadata: rule neighborhood

birth-survival-notation = "B" digits sep "S" digits     ; metadata: DROP first DROP DROP second
sb-notation = digits sep digits                     ; metadata: first DROP second

neighborhood = "V" / "H"  ; metadata: value

sep = "/"  ; metadata: DROP

digit = %x30-39  ; metadata: value
digits = *digit  ; metadata: digits
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class rulestring:
    rule: Any
    neighborhood: Any

    @classmethod
    def from_rule(cls, fields):
        rule, neighborhood = fields
        return cls(rule, neighborhood)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_rulestring(self)


@dataclass
class birth_survival_notation:
    first: Any
    second: Any

    @classmethod
    def from_rule(cls, fields):
        _, first, _, _, second = fields
        return cls(first, second)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_birth_survival_notation(self)


@dataclass
class sb_notation:
    first: Any
    second: Any

    @classmethod
    def from_rule(cls, fields):
        first, _, second = fields
        return cls(first, second)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_sb_notation(self)


@dataclass
class neighborhood:
    value: Any

    @classmethod
    def from_rule(cls, fields):
        value = fields
        return cls(value)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_neighborhood(self)


@dataclass
class sep:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_sep(self)


@dataclass
class digit:
    value: Any

    @classmethod
    def from_rule(cls, fields):
        value = fields
        return cls(value)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_digit(self)


@dataclass
class digits:
    digits: Any

    @classmethod
    def from_rule(cls, fields):
        digits = fields
        return cls(digits)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_digits(self)


class Visitor:
    def visit_rulestring(self, node: rulestring):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_rulestring."
        )

    def visit_birth_survival_notation(self, node: birth_survival_notation):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_birth_survival_notation."
        )

    def visit_sb_notation(self, node: sb_notation):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_sb_notation."
        )

    def visit_neighborhood(self, node: neighborhood):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_neighborhood."
        )

    def visit_sep(self, node: sep):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_sep."
        )

    def visit_digit(self, node: digit):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_digit."
        )

    def visit_digits(self, node: digits):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_digits."
        )


from parser_functions import Combinators, Stream
from parser_functions.combinators import FailResult, SuccessResult


class Parser(Combinators):
    @property
    def rulestring(self):
        return self._rulestring()

    def _rulestring(self):
        return self.map(rulestring.from_rule)(
            self.sequence(
                self.choice(
                    self.birth_survival_notation,
                    self.sb_notation,
                ),
                self.maybe(self.neighborhood),
            )
        )

    @property
    def birth_survival_notation(self):
        return self._birth_survival_notation()

    def _birth_survival_notation(self):
        return self.map(birth_survival_notation.from_rule)(
            self.sequence(
                self.word("B"),
                self.digits,
                self.sep,
                self.word("S"),
                self.digits,
            )
        )

    @property
    def sb_notation(self):
        return self._sb_notation()

    def _sb_notation(self):
        return self.map(sb_notation.from_rule)(
            self.sequence(
                self.digits,
                self.sep,
                self.digits,
            )
        )

    @property
    def neighborhood(self):
        return self._neighborhood()

    def _neighborhood(self):
        return self.map(neighborhood.from_rule)(
            self.choice(
                self.word("V"),
                self.word("H"),
            )
        )

    @property
    def sep(self):
        return self._sep()

    def _sep(self):
        return self.map(sep.from_rule)(self.word("/"))

    @property
    def digit(self):
        return self._digit()

    def _digit(self):
        return self.map(digit.from_rule)(self.regex("[\\x30-\\x39]"))

    @property
    def digits(self):
        return self._digits()

    def _digits(self):
        return self.map(digits.from_rule)(self.collect(self.zero_or_more((self.digit))))


def parse(value: str):
    parser = Parser()
    f = next(parser.rulestring(Stream.from_string(value)))
    match f:
        case FailResult(_):
            print(f)
        case SuccessResult(v, _):
            print(v)


def read_and_parse(path: str):
    with open(path, 'r', encoding='utf8') as f:
        data = f.read()
    parse(data)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--path', help='Path to file to parse.')
    group.add_argument('--data', help='Direct data to parse.')
    args = parser.parse_args()
    if args.path:
        read_and_parse(args.path)
    else:
        parse(args.data)


if __name__ == '__main__':
    main()

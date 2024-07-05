from dataclasses import dataclass
from enum import Enum
from typing import Optional, Set

from parser_functions.cellular_automata.parser import (
    Parser,
    Visitor,
    birth_survival_notation,
    digit,
    digits,
    neighborhood,
    rulestring,
    sb_notation,
)
from parser_functions.combinators import Stream


class Neighborhood(Enum):
    VON_NEUMANN = 1
    HEXAGONAL = 2

    @classmethod
    def from_symbol(cls, symbol):
        return {
            "V": Neighborhood.VON_NEUMANN,
            "H": Neighborhood.HEXAGONAL,
        }.get(symbol)


class RulesetVisitor(Visitor):

    def visit_rulestring(self, node: rulestring):
        birth, survival = node.rule.accept(self)
        match node.neighborhood:
            case None:
                n = None
            case neighborhood(value):
                n = Neighborhood.from_symbol(value)
        return birth, survival, n

    def visit_birth_survival_notation(self, node: birth_survival_notation):
        return node.first.accept(self), node.second.accept(self)

    def visit_sb_notation(self, node: sb_notation):
        return node.second.accept(self), node.first.accept(self)

    def visit_digits(self, node: digits):
        values = [d.accept(self) for d in node.digits]
        return values

    def visit_digit(self, node: digit):
        return int(node.value)


@dataclass
class CARuleSet:
    """Class representing a Cellular Automata rule set."""

    births: Set[int]
    survivals: Set[int]
    neighborhood: Optional[Neighborhood]

    @classmethod
    def from_rulestring(cls, node: rulestring):
        """Construct from a rulestring parser node."""
        visitor = RulesetVisitor()
        births, survivals, n = node.accept(visitor)
        return cls(set(births), set(survivals), n)

    @classmethod
    def from_string(cls, string: str):
        """Construct from a string."""
        p = Parser()
        r = next(p.rulestring(Stream.from_string(string)))
        return cls.from_rulestring(r.value)

    def does_survive(self, live_neighbors: int) -> bool:
        """Determines if a cell survives from the number of live neighbors it has."""
        return live_neighbors in self.survivals

    def is_born(self, live_neighbors: int) -> bool:
        """Determines if a cell is born from the number of live neighbors it has."""
        return live_neighbors in self.births

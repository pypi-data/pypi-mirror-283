from dataclasses import dataclass
from typing import Any, Union

from parser_functions import Combinators


@dataclass
class NumberNode:
    """AST node representing a single number."""

    value: float

    def evaluate(self):
        """Evaluate the number which is just its value."""
        return self.value


@dataclass
class BinaryNode:
    """Ast node representing an operation (+-*/)"""

    op: str
    left: Union[NumberNode, 'BinaryNode']
    right: Union[NumberNode, 'BinaryNode']

    def _add(self, left, right):
        return left.evaluate() + right.evaluate()

    def _sub(self, left, right):
        return left.evaluate() - right.evaluate()

    def _mul(self, left, right):
        return left.evaluate() * right.evaluate()

    def _div(self, left, right):
        return left.evaluate() / right.evaluate()

    def _mod(self, left, right):
        return left.evaluate() % right.evaluate()

    def evaluate(self):
        """Evaluate the expression by applying the operation to left and right."""
        return {
            "+": self._add,
            "-": self._sub,
            "*": self._mul,
            "/": self._div,
            "%": self._mod,
        }.get(self.op)(self.left, self.right)


def isnode(node: Any) -> bool:
    """Return True if a object is a NumberNode or BinaryNode instance."""
    return isinstance(node, (NumberNode, BinaryNode))


def create_tree_node(args: Any) -> Union[BinaryNode, NumberNode]:
    """Take the output of the expr/term/factor and rules and wrap in a Node class."""
    if isinstance(args, (float, int)):
        return NumberNode(args)
    if isinstance(args, (NumberNode, BinaryNode)):
        return args

    match args:
        case [node, None] if isnode(node):
            return args[0]
        case [left, [op, right]] if isnode(left) and isnode(right):
            return BinaryNode(op, left, right)

    raise ValueError(f"Handle case {args} in create_tree_node")


class Arithmetic(Combinators):
    @property
    def number(self):
        """Match a number.

        Wraps the parent class number parser with token and also allows for unary."""
        return self.choice(
            self.token(super().number),
            self.map(lambda v: v[1] if v[0] is None else -v[1])(
                self.sequence(self.maybe(self.minus), self.token(super().number))
            ),
        )

    @property
    def l_paren(self):
        """Match ("""
        return self.token(self.char('('))

    @property
    def r_paren(self):
        """Match )"""
        return self.token(self.char(')'))

    @property
    def mul_div(self):
        """Match *, / or %"""
        return self.choice(
            self.token(self.char('*')),
            self.token(self.char('/')),
            self.token(self.char('%')),
        )

    @property
    def minus(self):
        """Match -"""
        return self.token(self.char('-'))

    @property
    def add_sub(self):
        """Match + or -"""
        return self.choice(
            self.token(self.char('+')),
            self.minus,
        )

    @property
    def expr(self):
        """Match an expression."""
        return self._expr()

    def _expr(self):
        return self.map(create_tree_node)(
            self.sequence(
                self.term,
                self.maybe(self.sequence(self.add_sub, self.term)),
            )
        )

    @property
    def term(self):
        """Match a term."""
        return self.map(create_tree_node)(
            self.sequence(
                self.factor,
                self.maybe(self.sequence(self.mul_div, self.factor)),
            )
        )

    @property
    def factor(self):
        """Match a factor."""
        return self.map(create_tree_node)(
            self.choice(
                self.number,
                self.sequence(
                    self.l_paren, self.defer(self._expr), self.r_paren, take=1
                ),
            )
        )

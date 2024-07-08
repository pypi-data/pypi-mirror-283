"""AST node classes for parts of an ABNF grammar."""

from abc import ABC
from dataclasses import dataclass
from typing import Any, List, Optional, Protocol

from parser_functions.combinators import Combinators, FailResult, Stream, SuccessResult


class CommentMetadata(Combinators):
    @property
    def metadata(self):
        return self.sequence(
            self.sp,
            self.word('metadata:'),
            self.sp,
            self.collect(self.zero_or_more(self.rule)),
            take=3,
        )

    @property
    def sp(self):
        return self.collect(
            self.zero_or_more(
                self.choice(
                    self.char(' '),
                    self.char('\t'),
                )
            )
        )

    @property
    def rule(self):
        return self.sequence(
            self.join(
                self.collect(
                    self.one_or_more(
                        self.choice(
                            self.letter,
                            self.char('_'),
                        )
                    )
                )
            ),
            self.sp,
            take=0,
            flatten=True,
        )


def convert_pascal_case_to_snake_case(name: str) -> str:
    return ''.join(['_' + i.lower() if i.isupper() else i for i in name]).lstrip('_')


def convert_snake_case_to_pascal_case(name: str) -> str:
    return ''.join(
        [
            seg.capitalize() if any(c.islower() for c in seg) else seg
            for seg in name.split('_')
        ]
    )


class HasVisit(Protocol):
    pass


@dataclass
class ASTNode(ABC):
    def accept(self, visitor: HasVisit):
        name = convert_pascal_case_to_snake_case(self.__class__.__name__)
        return getattr(visitor, f'visit_{name}')(self)


@dataclass
class HexNode(ASTNode):
    value: str
    rest: Optional[Any]

    @classmethod
    def from_rule(cls, fields):
        return cls(*fields)


@dataclass
class CharValNode(ASTNode):
    value: str

    @classmethod
    def from_rule(cls, fields):
        return cls(fields)


@dataclass
class RuleNameNode(ASTNode):
    name: str
    node_name: str
    function_name: str

    @classmethod
    def from_rule(cls, name):
        return cls(
            name,
            convert_snake_case_to_pascal_case(name.replace('-', '_')) + 'Node',
            name.replace('-', '_').lower(),
        )


@dataclass
class DeferNode(ASTNode):
    target: ASTNode


@dataclass
class AlternationNode(ASTNode):

    nodes: List[ASTNode]

    @classmethod
    def from_rule(cls, fields):
        return cls(fields)


@dataclass
class GroupNode(ASTNode):
    target: AlternationNode

    @classmethod
    def from_rule(cls, fields):
        return cls(fields)


@dataclass
class OptionNode(ASTNode):
    target: AlternationNode

    @classmethod
    def from_rule(cls, fields):
        return cls(fields)


@dataclass
class ConcatenationNode(ASTNode):

    nodes: List[ASTNode]

    @classmethod
    def from_rule(cls, fields):
        return cls(fields)


@dataclass
class RepititionNode(ASTNode):
    target: ASTNode
    lower: Optional[int]
    upper: Optional[int]

    @classmethod
    def from_rule(cls, fields):
        repeat, target = fields
        match repeat:
            case None:
                lower, upper = 1, 1
            case [None, None]:
                lower, upper = None, None
            case [a, None]:
                lower, upper = int(a), None
            case [None, b]:
                lower, upper = None, int(b)
            case [a, b]:
                lower, upper = int(a), int(b)
            case a:
                ia = int(a)
                lower, upper = ia, ia
        return cls(target, lower, upper)


@dataclass
class RuleNode(ASTNode):
    name_node: RuleNameNode
    rhs: AlternationNode
    metadata: List[str]

    def metadata_for_field(self, n: int):
        try:
            data = self.metadata[n]
            return data
        except IndexError:
            return None

    def fields(self):
        fields = []
        rhs = self.rhs.nodes[0]
        for i, _ in enumerate(rhs.nodes):
            rename = self.metadata_for_field(i)
            field_name = rename if rename else f'field_{i+1}'
            if rename == 'DROP':
                field_name = '_'
            fields.append(field_name)
        return fields

    @classmethod
    def _process_comment(cls, comment):
        cm = CommentMetadata()
        r = next(cm.metadata(Stream.from_string(comment)))
        match r:
            case FailResult(_):
                return []
            case SuccessResult(v, _):
                return v
        return r.value

    @classmethod
    def from_rule(cls, fields):
        fields = [
            fields[0],
            fields[1][0],
            cls._process_comment(fields[1][1]),
        ]
        return cls(*fields)


@dataclass
class RuleListNode(ASTNode):
    rules: List[RuleNode]

    @classmethod
    def from_rule(cls, fields):
        return cls([rule for rule in fields if isinstance(rule, RuleNode)])

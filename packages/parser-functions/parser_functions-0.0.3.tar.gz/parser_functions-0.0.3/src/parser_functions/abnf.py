import sys
import textwrap
from abc import ABC
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, List, Optional, Protocol

from parser_functions.combinators import (
    Combinators,
    FailResult,
    Stream,
    SuccessResult,
    add_spy,
)

c = Combinators()


@dataclass
class ASTNode(ABC):
    pass


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

    @classmethod
    def from_rule(cls, name):
        return cls(name.replace('-', '_'))


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
                upper, lower = None, None
            case [a, None]:
                upper, lower = int(a), None
            case [None, b]:
                upper, lower = None, int(b)
            case [a, b]:
                upper, lower = int(a), int(b)
            case a:
                ia = int(a)
                lower, upper = ia, ia
        return cls(target, lower, upper)


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

        return self.join(
            self.collect(self.one_or_more(self.choice(self.letter, self.char('_'))))
        )


@dataclass
class RuleNode(ASTNode):
    name_node: RuleNameNode
    binding: str
    rhs: ASTNode
    metadata: List[str]

    def metadata_for_field(self, n: int):
        try:
            data = self.metadata[n]
            return data
        except IndexError:
            return None

    def fields(self):
        fields = []
        rhs: ConcatenationNode = self.rhs.nodes[0]
        for i, node in enumerate(rhs.nodes):
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
            fields[1],
            fields[2][0],
            cls._process_comment(fields[2][1]),
        ]
        return cls(*fields)


@dataclass
class RuleListNode(ASTNode):
    rules: List[RuleNode]

    @classmethod
    def from_rule(cls, fields):
        return cls([rule for rule in fields if isinstance(rule, RuleNode)])


class Writer(Protocol):
    def write(self, value: str):
        pass


class IndentWriter(Protocol):
    def write(self, value: str, indent: int):
        pass


@dataclass
class TextWrapIndentWriter(IndentWriter):
    writer: Writer

    def write(self, value, indent):
        self.writer.write(textwrap.wrap(value, initial_indent=indent))


@dataclass
class CodeGen:
    writer: Writer = field(
        default_factory=lambda: sys.stdout,
    )
    _indent: int = 0
    _d_indent: int = 4

    def write(self, value: str, indent=None):
        if indent is None:
            indent = self._indent
        self.writer.write(textwrap.indent(value, prefix=' ' * indent))

    @contextmanager
    def indented(self, amt=1):
        try:
            self.indent(amt)
            yield
        finally:
            self.dedent(amt)

    def indent(self, amt=1):
        self._indent += self._d_indent * amt

    def dedent(self, amt=1):
        self._indent -= self._d_indent * amt

    def _rename(self, name):
        result = []
        last_matched = True
        for old, new in zip(name, name.lower()):
            if old == new:
                result.append(old)
                last_matched = True
            else:
                if last_matched:
                    result.append('_')
                    result.append(new)
                else:
                    result.append(new)
                last_matched = False
        return ''.join(result)

    def generate(self, node: ASTNode, indent_hint=True):
        node_name = self._rename(node.__class__.__name__)
        handler_name = f'_generate{node_name}'
        getattr(self, handler_name, self._unknown)(node, indent_hint)

    def _unknown(self, node: ASTNode, _):
        print(f'Unknown ast node: {node.__class__.__name__}')


@dataclass
class ParserFileGenerator(CodeGen):
    file_data: str = ""
    nodes: CodeGen = field(init=False)
    visitors: CodeGen = field(init=False)
    parser: CodeGen = field(init=False)

    def __post_init__(self):
        self.nodes = NodeGen(self.writer)
        self.visitors = VisitorGen(self.writer)
        self.parser = ParserGen(self.writer)

    def generate(self, node: ASTNode, indent_hint=True):
        self._write_module_docstring()
        self.nodes.generate(node, indent_hint)
        self.visitors.generate(node, indent_hint)
        self.parser.generate(node, indent_hint)

    def _write_module_docstring(self):
        if not self.file_data:
            return
        self.write('"""')
        self.write('File code generated from ABNF grammar:\n\n')
        self.write(self.file_data)
        self.write('"""\n')


@dataclass
class VisitorGen(CodeGen):

    def _generate_rule_list_node(self, node: RuleListNode, indent_hint):
        self.write('class Visitor:\n')
        for rule in node.rules:
            name = rule.name_node.name
            with self.indented():
                self.write(f'def visit_{name}(self, node: {name}):\n')
                with self.indented():
                    error_msg = (
                        f"{{self.__class__.__name__}} does not implement visit_{name}."
                    )
                    self.write('raise NotImplementedError(\n')
                    with self.indented():
                        self.write(f'f"{error_msg}"\n')
                    self.write(')\n\n')

        self.write('\n')


@dataclass
class NodeGen(CodeGen):
    def _classname(self, name):
        return name.capitalize()

    def _generate_rule_list_node(self, node: RuleListNode, indent_hint):
        self.write('from typing import Any\n')
        self.write('from dataclasses import dataclass\n\n\n')
        for rule in node.rules:
            self.generate(rule)

    def _generate_rule_node(self, node: RuleNode, indent_hint):
        self.write('@dataclass\n' f'class {node.name_node.name}:\n')
        self._gen_types(node)
        with self.indented():
            self.write('@classmethod\n')
            self.write('def from_rule(cls, fields):\n')
            with self.indented():
                self.write(f'{", ".join(node.fields())} = fields\n')
                self.write(
                    f'return cls({", ".join(f for f in node.fields() if f != "_")})'
                )

            self.write('\n\n')
            self.write('def accept(self, visitor: "Visitor"):\n')
            with self.indented():
                self.write(f'return visitor.visit_{node.name_node.name}(self)\n\n')
        self.write('\n')

    def _gen_types(self, rule: RuleNode):
        with self.indented():
            for field_name in rule.fields():
                if field_name == '_':
                    continue
                self.write(f'{field_name}: Any\n')
        self.write('\n')


class ParserGen(CodeGen):
    def _generate_rule_list_node(self, node: RuleListNode, indent_hint):
        self.write('from parser_functions import Combinators, Stream\n')
        self.write(
            'from parser_functions.combinators import FailResult, SuccessResult\n\n\n'
        )
        self.write('class Parser(Combinators):\n')
        with self.indented():
            for rule in node.rules:
                self.generate(rule)
        main = node.rules[0].name_node.name
        self.write(
            "\n"
            "def parse(value: str):\n"
            "    parser = Parser()\n"
            f"    f = next(parser.{main}(Stream.from_string(value)))\n"
            "    match f:\n"
            "        case FailResult(_):\n"
            "            print(f)\n"
            "        case SuccessResult(v, _):\n"
            "            print(v)\n"
            "\n"
            "\n"
            "def read_and_parse(path: str):\n"
            "    with open(path, 'r', encoding='utf8') as f:\n"
            "        data = f.read()\n"
            "    parse(data)\n"
            "\n"
            "\n"
            "def main():\n"
            "    import argparse\n"
            "    parser = argparse.ArgumentParser()\n"
            "    group = parser.add_mutually_exclusive_group()\n"
            "    group.add_argument('--path', help='Path to file to parse.')\n"
            "    group.add_argument('--data', help='Direct data to parse.')\n"
            "    args = parser.parse_args()\n"
            "    if args.path:\n"
            "        read_and_parse(args.path)\n"
            "    else:\n"
            "        parse(args.data)\n"
            "\n"
            "\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
        )

    def _generate_rule_node(self, node: RuleNode, indent_hint):
        self.write('@property\n' f'def {node.name_node.name}(self):\n')
        self.indent()
        self.write(f'return self._{node.name_node.name}()\n')
        self.dedent()
        self.write('\n' f'def _{node.name_node.name}(self):\n')
        self.indent()
        self.write(f'return self.map({node.name_node.name}.from_rule)(')
        self.generate(node.rhs, indent_hint=False)
        self.dedent()
        self.write(')\n\n', indent=0)

    def _generate_alternation_node(self, node: AlternationNode, indent_hint):
        # Everything is wrapped in an AlternationNode, so if there is only
        # one node we can just unwrap it and generate from there.
        if len(node.nodes) == 1:
            self.generate(node.nodes[0], indent_hint)
            return

        # If there are more than 1 alternative then we need to construct a choice.
        self.write('self.choice(\n', indent=None if indent_hint else 0)
        with self.indented():
            for child in node.nodes:
                self.generate(child)
                self.write(',\n', indent=0)
        self.write(')')

    def _generate_concatenation_node(self, node: ConcatenationNode, indent_hint):
        # Everything is wrapped in an concat node, so if there is only
        # one node we can just unwrap it and generate from there.
        if len(node.nodes) == 1:
            self.generate(node.nodes[0], indent_hint)
            return

        # If there are more than one then we make each node an argument to
        # self.sequence.
        self.write('self.sequence(\n', indent=None if indent_hint else 0)
        with self.indented():
            for child in node.nodes:
                self.generate(child)
                self.write(',\n', indent=0)
        self.write(')')

    def _generate_repitition_node(self, node: RepititionNode, indent_hint):
        match node:
            # Repeated once means we can just ignore the RepititionNode
            case RepititionNode(child, 1, 1):
                self.generate(child, indent_hint)

            # [None, None] maps to [zero, infinity] which is zero_or_more
            case RepititionNode(child, None, None):
                self.write(
                    'self.collect(self.zero_or_more((',
                    indent=None if indent_hint else 0,
                )
                self.generate(child, indent_hint=False)
                self.write(')))', indent=0)

            # If upper and lower bounds (n, m) are the same then this is just an
            # element repeated n times. We can jsut remap this to a ConcatenationNode.
            case RepititionNode(child, n, m) if n == m and n is not None:
                self.generate(ConcatenationNode([child for _ in range(n)]))
            case _:
                raise ValueError(f'unknown Repitition({node.lower}, {node.upper})')

    def _generate_group_node(self, node: GroupNode, indent_hint):
        # Group nodes are a syntactic construct and are just pass-through in
        # the AST.
        self.generate(node.target, indent_hint)

    def _generate_option_node(self, node: GroupNode, indent_hint):
        self.write('self.maybe(')
        self.generate(node.target, indent_hint=False)
        self.write(')', indent=0)

    def _generate_rule_name_node(self, node: RuleNameNode, indent_hint):
        self.write(f'self.{node.name}', indent=None if indent_hint else 0)

    def _generate_hex_node(self, node: HexNode, indent_hint):
        match node.rest:
            case None:
                self.write(
                    f'self.regex("\\\\x{node.value}")',
                    indent=None if indent_hint else 0,
                )
            case ['-', other]:
                self.write(
                    f'self.regex("[\\\\x{node.value}-\\\\x{other}]")',
                    indent=None if indent_hint else 0,
                )
            case _:
                raise ValueError(f'Unsuported hex node: {node}')

    def _generate_char_val_node(self, node: CharValNode, indent_hint):
        self.write(f'self.word("{node.value}")', indent=None if indent_hint else 0)

    def _unknown(self, node: ASTNode, _):
        print(f'Unknown ast node: {node.__class__.__name__}')


class ABNFCore(Combinators):

    @property
    def alpha(self):
        """Match A-Z or a-z"""
        return self.letter

    @property
    def bit(self):
        """Match 0 or 1."""
        return self.choice(
            self.char('0'),
            self.char('1'),
        )

    @property
    def bits(self):
        """Match 1 or more bit."""
        return self.join(self.collect(self.one_or_more(self.bit)))

    @property
    def character(self):
        """Match any 7 bit ascii character excluding NULL"""
        return self.regex('[\x01-\x7f]')

    @property
    def cr(self):
        """Match carriage return"""
        return self.char('\r')

    @property
    def crlf(self):
        """Mtch cr followed by lf"""
        return self.sequence(
            self.cr,
            self.lf,
        )

    @property
    def ctl(self):
        """Match control byte"""
        return self.choice(
            self.regex('[\x00-\x1f]'),
            self.regex('\x7f'),
        )

    @property
    def dquote(self):
        """Match double quote"""
        return self.char('"')

    @property
    def hexdig(self):
        """Match a hex digit"""
        return self.choice(
            self.digit,
            self.char("A"),
            self.char("B"),
            self.char("C"),
            self.char("D"),
            self.char("E"),
            self.char("F"),
        )

    @property
    def hexdigs(self):
        """Match one or more hex digits"""
        return self.join(self.collect(self.one_or_more(self.hexdig)))

    @property
    def htab(self):
        """Match horizontal tab"""
        return self.char('\t')

    @property
    def lf(self):
        """Match line feed"""
        return self.char('\n')

    @property
    def lwsp(self):
        """Match linear white space.

        Use of this linear-white-space rule permits lines containing only white space
        that are no longer legal in mail headers and have caused interoperability
        problems in other contexts.

        Do not use when defining mail headers and use with caution in other contexts.
        """
        return self.collect(
            self.zero_or_more(
                self.choice(
                    self.wsp,
                    self.sequence(self.crlf, self.wsp),
                )
            )
        )

    @property
    def octet(self):
        """Match 8 bits of data"""
        return self.regex('[\x00-\xFF]')

    @property
    def sp(self):
        """Match space"""
        return self.char(' ')

    @property
    @add_spy
    def vchar(self):
        """Match visible character"""
        return self.regex('[\x21-\x7e]')

    @property
    @add_spy
    def vchar_without_dquote(self):
        """Match visible character except dqoute"""
        return self.regex('[\x21-\x21\x23-\x7e]')

    @property
    def wsp(self):
        """Match white space"""
        return self.choice(
            self.sp,
            self.htab,
        )


class ABNF(ABNFCore):

    @property
    def ws(self):
        return self.collect(
            self.one_or_more(
                self.choice(
                    self.sp,
                    self.nl,
                    self.comment,
                )
            )
        )

    @property
    def sp(self):
        """Match one or more space or tab."""
        return self.collect(
            self.one_or_more(self.choice(self.char(' '), self.char('\t')))
        )

    @property
    def nl(self):
        """Match \n or \r\n"""
        return self.choice(
            self.char('\n'),
            self.sequence(self.char('\r'), self.char('\n')),
        )

    @property
    def not_nl(self):
        """Match everything except \n and \r"""
        return self.all_except(['\n', '\r'])

    @property
    def br(self):
        """Match line break followed by whitespace"""
        return self.sequence(
            self.maybe(self.sp),
            self.choice(self.comment, self.nl),
            self.maybe(self.ws),
            take=1,
        )

    @property
    @add_spy
    def comment(self):
        """Match a comment"""
        return self.join(
            self.sequence(
                self.char(';'),
                self.collect(self.zero_or_more(self.not_nl)),
                self.nl,
                take=1,
            )
        )

    @property
    @add_spy
    def rulelist(self):
        """Match list of rules."""
        return self.map(RuleListNode.from_rule)(
            self.sequence(
                self.maybe(self.ws),
                self.collect(self.zero_or_more(self.rule)),
                take=1,
            )
        )

    @property
    @add_spy
    def rule(self):
        """Match ABNF rule."""
        return self.map(RuleNode.from_rule)(
            self.sequence(
                self.rulename,
                self.defined_as,
                self.elements,
                take=[0, 1, 2],
            )
        )

    @property
    def rulename(self):
        """Match rulename."""
        return self.map(RuleNameNode.from_rule)(
            self.join(
                self.sequence(
                    self.alpha,
                    self.collect(
                        self.zero_or_more(
                            self.choice(
                                self.alpha,
                                self.digit,
                                self.char("-"),
                            )
                        )
                    ),
                    flatten=True,
                )
            )
        )

    @property
    def defined_as(self):
        """Basic rules definition and incremental alternatives"""
        return self.sequence(
            self.sp,
            self.choice(
                self.char('='),
                self.word('=/'),
            ),
            self.sp,
            take=1,
        )

    @property
    def elements(self):
        return self.sequence(
            self.alternation,
            self.br,
        )

    @property
    def alternation(self):
        return self._alternation()

    def _alternation(self):
        return self.map(AlternationNode.from_rule)(
            self.sequence(
                self.concatenation,
                self.collect(
                    self.zero_or_more(
                        self.sequence(
                            self.maybe(self.sp),
                            self.char('/'),
                            self.maybe(self.sp),
                            self.concatenation,
                            take=3,
                        )
                    )
                ),
                flatten=True,
            )
        )

    @property
    def concatenation(self):
        return self.map(ConcatenationNode.from_rule)(
            self.sequence(
                self.repitition,
                self.collect(
                    self.zero_or_more(
                        self.sequence(
                            self.maybe(self.sp),
                            self.repitition,
                            take=1,
                        )
                    )
                ),
                flatten=True,
            )
        )

    @property
    def repitition(self):
        return self.map(RepititionNode.from_rule)(
            self.sequence(
                self.maybe(self.repeat),
                self.element,
            )
        )

    @property
    def repeat(self):
        return self.choice(
            self.digits,
            self.sequence(
                self.maybe(self.digits),
                self.char('*'),
                self.maybe(self.digits),
                take=[0, 2],
            ),
        )

    @property
    def element(self):
        return self.choice(
            self.spy('rulename: {}\n')(self.rulename),
            self.group,
            self.option,
            self.char_val,
            self.num_val,
            self.prose_val,
        )

    @property
    def group(self):
        return self.map(GroupNode.from_rule)(
            self.sequence(
                self.char('('),
                self.maybe(self.sp),
                self.defer(self._alternation),
                self.maybe(self.sp),
                self.char(')'),
                take=2,
            )
        )

    @property
    def option(self):
        return self.map(OptionNode.from_rule)(
            self.sequence(
                self.char('['),
                self.maybe(self.sp),
                self.defer(self._alternation),
                self.maybe(self.sp),
                self.char(']'),
                take=2,
            )
        )

    @property
    @add_spy
    def char_val(self):
        """Match quoted string without double quote."""
        return self.map(CharValNode.from_rule)(
            self.join(
                self.sequence(
                    self.dquote,
                    self.collect(
                        self.zero_or_more(
                            self.choice(
                                self.nl,
                                self.vchar_without_dquote,
                            )
                        )
                    ),
                    self.dquote,
                    take=1,
                )
            )
        )

    @property
    def num_val(self):
        """Match numeric value"""
        return self.sequence(
            self.char('%'),
            self.choice(
                self.bin_val,
                self.dec_val,
                self.hex_val,
            ),
            take=1,
        )

    @property
    def bin_val(self):
        """Match binary value"""
        return self.sequence(
            self.char('b'),
            self.bits,
            self.maybe(
                self.choice(
                    self.collect(
                        self.one_or_more(
                            self.sequence(
                                self.char('.'),
                                self.bits,
                            )
                        )
                    ),
                    self.sequence(
                        self.char('-'),
                        self.bits,
                    ),
                )
            ),
        )

    @property
    def dec_val(self):
        """Match decimal value."""
        return self.sequence(
            self.char('d'),
            self.digits,
            self.maybe(
                self.choice(
                    self.collect(
                        self.one_or_more(
                            self.sequence(
                                self.char('.'),
                                self.digits,
                            )
                        )
                    ),
                    self.sequence(
                        self.char('-'),
                        self.digits,
                    ),
                )
            ),
        )

    @property
    def hex_val(self):
        """Match hex value."""
        return self.map(HexNode.from_rule)(
            self.sequence(
                self.char('x'),
                self.hexdigs,
                self.maybe(
                    self.choice(
                        self.collect(
                            self.one_or_more(
                                self.sequence(
                                    self.char('.'),
                                    self.hexdigs,
                                )
                            )
                        ),
                        self.sequence(
                            self.char('-'),
                            self.hexdigs,
                        ),
                    )
                ),
                take=[1, 2],
            )
        )

    @property
    def prose_val(self):
        """Match prose value.

        Bracketed string of SP and VCHAR without angles.
        Prose description, to be uesd as a last resort.
        """
        return self.sequence(
            self.char('<'),
            self.collect(
                self.zero_or_more(
                    self.choice(
                        self.regex('[\x20-\x3D]'),
                        self.regex('[\x3F-\x7E]'),
                    )
                )
            ),
            self.char('>'),
        )

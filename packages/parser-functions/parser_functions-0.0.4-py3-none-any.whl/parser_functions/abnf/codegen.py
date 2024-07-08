"""Code generator visitor class to generate parser code from an ABNF class."""

import sys
import textwrap
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Protocol

from .ast import (
    AlternationNode,
    ASTNode,
    CharValNode,
    ConcatenationNode,
    DeferNode,
    GroupNode,
    HexNode,
    RepititionNode,
    RuleListNode,
    RuleNameNode,
    RuleNode,
)


class Writer(Protocol):
    def write(self, value: str):
        pass


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
        self.write('"""  # noqa\n')


@dataclass
class VisitorGen(CodeGen):

    def _generate_rule_list_node(self, node: RuleListNode, _):
        self.write('from abc import ABC\n')
        self.write('class Visitor(ABC):\n')
        for rule in node.rules:
            name = rule.name_node.function_name
            with self.indented():
                self.write(
                    f'def visit_{name}(self, node: {rule.name_node.node_name}):\n'
                )
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
    def _generate_rule_list_node(self, node: RuleListNode, _):
        self.write('from typing import Any\n')
        self.write('from dataclasses import dataclass\n\n\n')
        for rule in node.rules:
            self.generate(rule)

    def _generate_rule_node(self, node: RuleNode, _):
        self.write('@dataclass\n' f'class {node.name_node.node_name}:\n')
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
                self.write(
                    f'return visitor.visit_{node.name_node.function_name}(self)\n\n'
                )
        self.write('\n')

    def _gen_types(self, rule: RuleNode):
        with self.indented():
            for field_name in rule.fields():
                if field_name == '_':
                    continue
                self.write(f'{field_name}: Any\n')
        self.write('\n')


@dataclass
class ParserGen(CodeGen):

    use_property_calls: bool = True

    @contextmanager
    def defer_calls(self):
        try:
            self.use_property_calls = False
            yield
        finally:
            self.use_property_calls = True

    def _generate_rule_list_node(self, node: RuleListNode, _):
        self.write('from parser_functions import Stream\n')
        self.write('from parser_functions.abnf.parser import ABNFCore\n')
        self.write(
            'from parser_functions.combinators import FailResult, SuccessResult\n\n\n'
        )
        self.write('class Parser(ABNFCore):\n')
        with self.indented():
            for rule in node.rules:
                self.generate(rule)
        main = node.rules[0].name_node.function_name
        self.write(
            "\n"
            "def parse(value: str):\n"
            "    parser = Parser()\n"
            f"    f = next(parser.{main}(Stream.from_string(value)))\n"
            "    match f:\n"
            "        case FailResult(s):\n"
            "            print(s)\n"
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

    def _generate_rule_node(self, node: RuleNode, _):
        self.write('@property\n' f'def {node.name_node.function_name}(self):\n')
        self.indent()
        self.write(f'return self._{node.name_node.function_name}()\n')
        self.dedent()
        self.write('\n' f'def _{node.name_node.function_name}(self):\n')
        self.indent()
        self.write(f'return self.map({node.name_node.node_name}.from_rule)(')
        self.generate(node.rhs, indent_hint=False)
        self.dedent()
        self.write(')\n\n', indent=0)

    def _generate_defer_node(self, node: DeferNode, indent_hint):
        self.write('self.defer(', indent=None if indent_hint else 0)
        with self.defer_calls():
            self.generate(node.target, indent_hint=False)
        self.write(')', indent=0)

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

            case RepititionNode(child, 1, None):
                self.write(
                    'self.collect(self.one_or_more((',
                    indent=None if indent_hint else 0,
                )
                self.generate(child, indent_hint=False)
                self.write(')))', indent=0)
            case _:
                raise ValueError(f'unknown Repitition({node.lower}, {node.upper})')

    def _generate_group_node(self, node: GroupNode, indent_hint):
        # Group nodes are a syntactic construct and are just pass-through in
        # the AST.
        self.generate(node.target, indent_hint)

    def _generate_option_node(self, node: GroupNode, _):
        self.write('self.maybe(')
        self.generate(node.target, indent_hint=False)
        self.write(')', indent=0)

    def _generate_rule_name_node(self, node: RuleNameNode, indent_hint):
        if self.use_property_calls:
            call = f'self.{node.function_name}'
        else:
            call = f'self._{node.function_name}'
        self.write(call, indent=None if indent_hint else 0)

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

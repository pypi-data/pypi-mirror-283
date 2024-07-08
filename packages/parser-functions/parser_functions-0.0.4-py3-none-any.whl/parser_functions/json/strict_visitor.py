import argparse

from parser_functions.combinators import FailResult, Stream, SuccessResult
from parser_functions.json.strict_parser import (
    ArrayNode,
    EscapeNode,
    ExpNode,
    FalseNode,
    IntNode,
    JSONTextNode,
    MemberNode,
    MinusNode,
    NullNode,
    NumberNode,
    ObjectNode,
    Parser,
    StringNode,
    TrueNode,
    UnescapedNode,
    ValueNode,
    Visitor,
    ZeroNode,
)


class JSONVisitor(Visitor):
    """Converts a JSONTextNode into a Python dictionary."""

    def visit_json_text(self, node: JSONTextNode):
        return node.value.accept(self)

    def visit_array(self, node: ArrayNode):
        head, tail = node.value
        result = [value.accept(self) for value in [head] + [v[1] for v in tail]]
        return result

    def visit_object(self, node: ObjectNode):
        head, tail = node.value
        result = [member.accept(self) for member in [head] + [v[1] for v in tail]]
        return dict(result)

    def visit_member(self, node: MemberNode):
        key = node.key.accept(self)
        value = node.value.accept(self)
        return [key, value]

    def visit_string(self, node: StringNode):
        def _pick_char(child):
            match child.value:
                case UnescapedNode(char):
                    return char
                case [EscapeNode(), char]:
                    return f"\\{char}".encode().decode('unicode_escape')

        return ''.join([_pick_char(child) for child in node.value])

    def visit_number(self, node: NumberNode):
        value = node.value.accept(self)
        if node.frac:
            value += float('0.' + ''.join(node.frac.digits))
        match node.minus:
            case MinusNode():
                value *= -1
        if node.exponent:
            exp = node.exponent.accept(self)
            value **= exp
        return value

    def visit_exp(self, node: ExpNode):
        value = int(''.join(node.digits))
        match node.sign:
            case MinusNode():
                value *= -1
        return value

    def visit_int(self, node: IntNode):
        match node.value:
            case ZeroNode():
                return 0
            case [head, tail]:
                return int(''.join([head.digit] + tail))

    def visit_zero(self, node: ZeroNode):
        return 0

    def visit_value(self, node: ValueNode):
        match value := node.value:
            case FalseNode():
                return False
            case NullNode():
                return None
            case TrueNode():
                return True
            case _:
                return value.accept(self)


def parse(value: str):
    parser = Parser()
    f = next(parser.json_text(Stream.from_string(value)))
    match f:
        case FailResult(s):
            print(s)
            print(f)
        case SuccessResult(v, _):
            visitor = JSONVisitor()
            result = v.accept(visitor)
            print(result)


def read_and_parse(path: str):
    with open(path, 'r', encoding='utf8') as f:
        data = f.read()
    parse(data)


def main():
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

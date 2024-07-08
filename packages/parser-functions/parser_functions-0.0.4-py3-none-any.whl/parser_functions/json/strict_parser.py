"""File code generated from ABNF grammar:

JSON-text = ws value ws       ; metadata: DROP value DROP


begin-array     = ws %x5B ws  ; metadata: DROP DROP DROP
begin-object    = ws %x7B ws  ; metadata: DROP DROP DROP
end-array       = ws %x5D ws  ; metadata: DROP DROP DROP
end-object      = ws %x7D ws  ; metadata: DROP DROP DROP
name-separator  = ws %x3A ws  ; metadata: DROP DROP DROP
value-separator = ws %x2C ws  ; metadata: DROP DROP DROP


value = false / null / true / object / array / number / string  ; metadata: value
ws = whitespace  ; metadata: DROP
false = "false"  ; metadata: DROP
null  = "null"   ; metadata: DROP
true  = "true"   ; metadata: DROP


object = begin-object [ member *( value-separator member ) ] end-object ; metadata: DROP value DROP
member = string name-separator value                                    ; metadata: key DROP value
array = begin-array [ value *( value-separator value ) ] end-array      ; metadata: DROP value DROP


number = [ minus ] int [ frac ] [ exp ]  ; metadata: minus value frac exponent
decimal-point = "."               ; metadata: DROP
digit1-9 = %x31-39                ; metadata: digit
e = "E" / "e"                     ; metadata: DROP
frac = decimal-point 1*digit      ; metadata: DROP digits
exp = e [ minus / plus ] 1*digit  ; metadata: DROP sign digits
int = zero / ( digit1-9 *digit )  ; metadata: value
minus = "-"                       ; metadata: DROP
plus = "+"                        ; metadata: DROP
zero = "0"                        ; metadata: DROP


string = quotation-mark *character quotation-mark  ; metadata: DROP value DROP
character = unescaped / escape (%x22 / %x5C / %x2F / %x62 / %x66 / %x6E / %x72 / %x74 / %x75 4hexdig ) ; metadata: value
escape         = %x5C                         ; metadata: DROP
quotation-mark = %x22                         ; metadata: DROP
unescaped      = %x20-21 / %x23-5B / %x5D-FF  ; metadata: data
"""  # noqa

from abc import ABC
from dataclasses import dataclass
from typing import Any

from parser_functions import Stream
from parser_functions.abnf.parser import ABNFCore
from parser_functions.combinators import FailResult, SuccessResult


@dataclass
class JSONTextNode:
    value: Any

    @classmethod
    def from_rule(cls, fields):
        _, value, _ = fields
        return cls(value)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_json_text(self)


@dataclass
class BeginArrayNode:

    @classmethod
    def from_rule(cls, fields):
        _, _, _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_begin_array(self)


@dataclass
class BeginObjectNode:

    @classmethod
    def from_rule(cls, fields):
        _, _, _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_begin_object(self)


@dataclass
class EndArrayNode:

    @classmethod
    def from_rule(cls, fields):
        _, _, _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_end_array(self)


@dataclass
class EndObjectNode:

    @classmethod
    def from_rule(cls, fields):
        _, _, _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_end_object(self)


@dataclass
class NameSeparatorNode:

    @classmethod
    def from_rule(cls, fields):
        _, _, _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_name_separator(self)


@dataclass
class ValueSeparatorNode:

    @classmethod
    def from_rule(cls, fields):
        _, _, _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_value_separator(self)


@dataclass
class ValueNode:
    value: Any

    @classmethod
    def from_rule(cls, fields):
        value = fields
        return cls(value)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_value(self)


@dataclass
class WsNode:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_ws(self)


@dataclass
class FalseNode:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_false(self)


@dataclass
class NullNode:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_null(self)


@dataclass
class TrueNode:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_true(self)


@dataclass
class ObjectNode:
    value: Any

    @classmethod
    def from_rule(cls, fields):
        _, value, _ = fields
        return cls(value)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_object(self)


@dataclass
class MemberNode:
    key: Any
    value: Any

    @classmethod
    def from_rule(cls, fields):
        key, _, value = fields
        return cls(key, value)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_member(self)


@dataclass
class ArrayNode:
    value: Any

    @classmethod
    def from_rule(cls, fields):
        _, value, _ = fields
        return cls(value)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_array(self)


@dataclass
class NumberNode:
    minus: Any
    value: Any
    frac: Any
    exponent: Any

    @classmethod
    def from_rule(cls, fields):
        minus, value, frac, exponent = fields
        return cls(minus, value, frac, exponent)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_number(self)


@dataclass
class DecimalPointNode:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_decimal_point(self)


@dataclass
class Digit19Node:
    digit: Any

    @classmethod
    def from_rule(cls, fields):
        digit = fields
        return cls(digit)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_digit1_9(self)


@dataclass
class ENode:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_e(self)


@dataclass
class FracNode:
    digits: Any

    @classmethod
    def from_rule(cls, fields):
        _, digits = fields
        return cls(digits)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_frac(self)


@dataclass
class ExpNode:
    sign: Any
    digits: Any

    @classmethod
    def from_rule(cls, fields):
        _, sign, digits = fields
        return cls(sign, digits)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_exp(self)


@dataclass
class IntNode:
    value: Any

    @classmethod
    def from_rule(cls, fields):
        value = fields
        return cls(value)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_int(self)


@dataclass
class MinusNode:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_minus(self)


@dataclass
class PlusNode:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_plus(self)


@dataclass
class ZeroNode:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_zero(self)


@dataclass
class StringNode:
    value: Any

    @classmethod
    def from_rule(cls, fields):
        _, value, _ = fields
        return cls(value)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_string(self)


@dataclass
class CharacterNode:
    value: Any

    @classmethod
    def from_rule(cls, fields):
        value = fields
        return cls(value)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_character(self)


@dataclass
class EscapeNode:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_escape(self)


@dataclass
class QuotationMarkNode:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_quotation_mark(self)


@dataclass
class UnescapedNode:
    data: Any

    @classmethod
    def from_rule(cls, fields):
        data = fields
        return cls(data)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_unescaped(self)


class Visitor(ABC):
    def visit_json_text(self, node: JSONTextNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_json_text."
        )

    def visit_begin_array(self, node: BeginArrayNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_begin_array."
        )

    def visit_begin_object(self, node: BeginObjectNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_begin_object."
        )

    def visit_end_array(self, node: EndArrayNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_end_array."
        )

    def visit_end_object(self, node: EndObjectNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_end_object."
        )

    def visit_name_separator(self, node: NameSeparatorNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_name_separator."
        )

    def visit_value_separator(self, node: ValueSeparatorNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_value_separator."
        )

    def visit_value(self, node: ValueNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_value."
        )

    def visit_ws(self, node: WsNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_ws."
        )

    def visit_false(self, node: FalseNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_false."
        )

    def visit_null(self, node: NullNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_null."
        )

    def visit_true(self, node: TrueNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_true."
        )

    def visit_object(self, node: ObjectNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_object."
        )

    def visit_member(self, node: MemberNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_member."
        )

    def visit_array(self, node: ArrayNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_array."
        )

    def visit_number(self, node: NumberNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_number."
        )

    def visit_decimal_point(self, node: DecimalPointNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_decimal_point."
        )

    def visit_digit1_9(self, node: Digit19Node):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_digit1_9."
        )

    def visit_e(self, node: ENode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_e."
        )

    def visit_frac(self, node: FracNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_frac."
        )

    def visit_exp(self, node: ExpNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_exp."
        )

    def visit_int(self, node: IntNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_int."
        )

    def visit_minus(self, node: MinusNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_minus."
        )

    def visit_plus(self, node: PlusNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_plus."
        )

    def visit_zero(self, node: ZeroNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_zero."
        )

    def visit_string(self, node: StringNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_string."
        )

    def visit_character(self, node: CharacterNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_character."
        )

    def visit_escape(self, node: EscapeNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_escape."
        )

    def visit_quotation_mark(self, node: QuotationMarkNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_quotation_mark."
        )

    def visit_unescaped(self, node: UnescapedNode):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_unescaped."
        )


class Parser(ABNFCore):
    @property
    def json_text(self):
        return self._json_text()

    def _json_text(self):
        return self.map(JSONTextNode.from_rule)(
            self.sequence(
                self.ws,
                self.value,
                self.ws,
            )
        )

    @property
    def begin_array(self):
        return self._begin_array()

    def _begin_array(self):
        return self.map(BeginArrayNode.from_rule)(
            self.sequence(
                self.ws,
                self.regex("\\x5B"),
                self.ws,
            )
        )

    @property
    def begin_object(self):
        return self._begin_object()

    def _begin_object(self):
        return self.map(BeginObjectNode.from_rule)(
            self.sequence(
                self.ws,
                self.regex("\\x7B"),
                self.ws,
            )
        )

    @property
    def end_array(self):
        return self._end_array()

    def _end_array(self):
        return self.map(EndArrayNode.from_rule)(
            self.sequence(
                self.ws,
                self.regex("\\x5D"),
                self.ws,
            )
        )

    @property
    def end_object(self):
        return self._end_object()

    def _end_object(self):
        return self.map(EndObjectNode.from_rule)(
            self.sequence(
                self.ws,
                self.regex("\\x7D"),
                self.ws,
            )
        )

    @property
    def name_separator(self):
        return self._name_separator()

    def _name_separator(self):
        return self.map(NameSeparatorNode.from_rule)(
            self.sequence(
                self.ws,
                self.regex("\\x3A"),
                self.ws,
            )
        )

    @property
    def value_separator(self):
        return self._value_separator()

    def _value_separator(self):
        return self.map(ValueSeparatorNode.from_rule)(
            self.sequence(
                self.ws,
                self.regex("\\x2C"),
                self.ws,
            )
        )

    @property
    def value(self):
        return self._value()

    def _value(self):
        return self.map(ValueNode.from_rule)(
            self.choice(
                self.false,
                self.null,
                self.true,
                self.object,
                self.array,
                self.number,
                self.string,
            )
        )

    @property
    def ws(self):
        return self._ws()

    def _ws(self):
        return self.map(WsNode.from_rule)(self.whitespace)

    @property
    def false(self):
        return self._false()

    def _false(self):
        return self.map(FalseNode.from_rule)(self.word("false"))

    @property
    def null(self):
        return self._null()

    def _null(self):
        return self.map(NullNode.from_rule)(self.word("null"))

    @property
    def true(self):
        return self._true()

    def _true(self):
        return self.map(TrueNode.from_rule)(self.word("true"))

    @property
    def object(self):
        return self._object()

    def _object(self):
        return self.map(ObjectNode.from_rule)(
            self.sequence(
                self.begin_object,
                self.maybe(
                    self.sequence(
                        self.member,
                        self.collect(
                            self.zero_or_more(
                                (
                                    self.sequence(
                                        self.value_separator,
                                        self.member,
                                    )
                                )
                            )
                        ),
                    )
                ),
                self.end_object,
            )
        )

    @property
    def member(self):
        return self._member()

    def _member(self):
        return self.map(MemberNode.from_rule)(
            self.sequence(
                self.string,
                self.name_separator,
                self.defer(self._value),
            )
        )

    @property
    def array(self):
        return self._array()

    def _array(self):
        return self.map(ArrayNode.from_rule)(
            self.sequence(
                self.begin_array,
                self.maybe(
                    self.sequence(
                        self.defer(self._value),
                        self.collect(
                            self.zero_or_more(
                                (
                                    self.sequence(
                                        self.value_separator,
                                        self.defer(self._value),
                                    )
                                )
                            )
                        ),
                    )
                ),
                self.end_array,
            )
        )

    @property
    def number(self):
        return self._number()

    def _number(self):
        return self.map(NumberNode.from_rule)(
            self.sequence(
                self.maybe(self.minus),
                self.int,
                self.maybe(self.frac),
                self.maybe(self.exp),
            )
        )

    @property
    def decimal_point(self):
        return self._decimal_point()

    def _decimal_point(self):
        return self.map(DecimalPointNode.from_rule)(self.word("."))

    @property
    def digit1_9(self):
        return self._digit1_9()

    def _digit1_9(self):
        return self.map(Digit19Node.from_rule)(self.regex("[\\x31-\\x39]"))

    @property
    def e(self):
        return self._e()

    def _e(self):
        return self.map(ENode.from_rule)(
            self.choice(
                self.word("E"),
                self.word("e"),
            )
        )

    @property
    def frac(self):
        return self._frac()

    def _frac(self):
        return self.map(FracNode.from_rule)(
            self.sequence(
                self.decimal_point,
                self.collect(self.one_or_more((self.digit))),
            )
        )

    @property
    def exp(self):
        return self._exp()

    def _exp(self):
        return self.map(ExpNode.from_rule)(
            self.sequence(
                self.e,
                self.maybe(
                    self.choice(
                        self.minus,
                        self.plus,
                    )
                ),
                self.collect(self.one_or_more((self.digit))),
            )
        )

    @property
    def int(self):
        return self._int()

    def _int(self):
        return self.map(IntNode.from_rule)(
            self.choice(
                self.zero,
                self.sequence(
                    self.digit1_9,
                    self.collect(self.zero_or_more((self.digit))),
                ),
            )
        )

    @property
    def minus(self):
        return self._minus()

    def _minus(self):
        return self.map(MinusNode.from_rule)(self.word("-"))

    @property
    def plus(self):
        return self._plus()

    def _plus(self):
        return self.map(PlusNode.from_rule)(self.word("+"))

    @property
    def zero(self):
        return self._zero()

    def _zero(self):
        return self.map(ZeroNode.from_rule)(self.word("0"))

    @property
    def string(self):
        return self._string()

    def _string(self):
        return self.map(StringNode.from_rule)(
            self.sequence(
                self.quotation_mark,
                self.collect(self.zero_or_more((self.character))),
                self.quotation_mark,
            )
        )

    @property
    def character(self):
        return self._character()

    def _character(self):
        return self.map(CharacterNode.from_rule)(
            self.choice(
                self.unescaped,
                self.sequence(
                    self.escape,
                    self.choice(
                        self.regex("\\x22"),
                        self.regex("\\x5C"),
                        self.regex("\\x2F"),
                        self.regex("\\x62"),
                        self.regex("\\x66"),
                        self.regex("\\x6E"),
                        self.regex("\\x72"),
                        self.regex("\\x74"),
                        self.sequence(
                            self.regex("\\x75"),
                            self.sequence(
                                self.hexdig,
                                self.hexdig,
                                self.hexdig,
                                self.hexdig,
                            ),
                        ),
                    ),
                ),
            )
        )

    @property
    def escape(self):
        return self._escape()

    def _escape(self):
        return self.map(EscapeNode.from_rule)(self.regex("\\x5C"))

    @property
    def quotation_mark(self):
        return self._quotation_mark()

    def _quotation_mark(self):
        return self.map(QuotationMarkNode.from_rule)(self.regex("\\x22"))

    @property
    def unescaped(self):
        return self._unescaped()

    def _unescaped(self):
        return self.map(UnescapedNode.from_rule)(
            self.choice(
                self.regex("[\\x20-\\x21]"),
                self.regex("[\\x23-\\x5B]"),
                self.regex("[\\x5D-\\xFF]"),
            )
        )


def parse(value: str):
    parser = Parser()
    f = next(parser.json_text(Stream.from_string(value)))
    match f:
        case FailResult(s):
            print(s)
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

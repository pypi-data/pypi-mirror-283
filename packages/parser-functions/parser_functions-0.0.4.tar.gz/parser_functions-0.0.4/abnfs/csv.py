"""File code generated from ABNF grammar:

file = [header NL] record *tail-record [NL] ; metadata: header head_record tail_records DROP

header      = name *tail-name                ; metadata: head_name tail_names
record      = field *tail-field              ; metadata: head_field tail_fields
tail-record = NL record                      ; metadata: DROP record
name        = field                          ; metadata: field
tail-name   = COMMA name                     ; metadata: DROP name
field       = (escaped / non-escaped)        ; metadata: value
tail-field  = COMMA field                    ; metadata: DROP field

escaped     = DQUOTE *(TEXTDATA / COMMA / CR / LF / 2DQUOTE) DQUOTE ; metadata: DROP value DROP
non-escaped = *TEXTDATA                                             ; metadata: value

COMMA    = %x2C                         ; metadata: DROP
CR       = %x0D                         ; metadata: DROP
DQUOTE   = %x22                         ; metadata: DROP
LF       = %x0A                         ; metadata: DROP
CRLF     = CR LF                        ; metadata: DROP
NL       = (CRLF / LF)                  ; metadata: value
TEXTDATA =  %x20-21 / %x23-2B / %x2D-7E ; metadata: value
"""

import argparse
from dataclasses import dataclass
from typing import Any

from parser_functions import Combinators, Stream
from parser_functions.combinators import FailResult, SuccessResult


@dataclass
class file:
    header: Any
    head_record: Any
    tail_records: Any

    @classmethod
    def from_rule(cls, fields):
        header, head_record, tail_records, _ = fields
        return cls(header, head_record, tail_records)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_file(self)


@dataclass
class header:
    head_name: Any
    tail_names: Any

    @classmethod
    def from_rule(cls, fields):
        head_name, tail_names = fields
        return cls(head_name, tail_names)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_header(self)


@dataclass
class record:
    head_field: Any
    tail_fields: Any

    @classmethod
    def from_rule(cls, fields):
        head_field, tail_fields = fields
        return cls(head_field, tail_fields)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_record(self)


@dataclass
class tail_record:
    record: Any

    @classmethod
    def from_rule(cls, fields):
        _, record = fields
        return cls(record)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_tail_record(self)


@dataclass
class name:
    field: Any

    @classmethod
    def from_rule(cls, fields):
        field = fields
        return cls(field)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_name(self)


@dataclass
class tail_name:
    name: Any

    @classmethod
    def from_rule(cls, fields):
        _, name = fields
        return cls(name)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_tail_name(self)


@dataclass
class field:
    value: Any

    @classmethod
    def from_rule(cls, fields):
        value = fields
        return cls(value)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_field(self)


@dataclass
class tail_field:
    field: Any

    @classmethod
    def from_rule(cls, fields):
        _, field = fields
        return cls(field)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_tail_field(self)


@dataclass
class escaped:
    value: Any

    @classmethod
    def from_rule(cls, fields):
        _, value, _ = fields
        return cls(value)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_escaped(self)


@dataclass
class non_escaped:
    value: Any

    @classmethod
    def from_rule(cls, fields):
        value = fields
        return cls(value)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_non_escaped(self)


@dataclass
class COMMA:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_COMMA(self)


@dataclass
class CR:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_CR(self)


@dataclass
class DQUOTE:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_DQUOTE(self)


@dataclass
class LF:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()

    def accept(self, visitor: "Visitor"):
        return visitor.visit_LF(self)


@dataclass
class CRLF:
    field_2: Any

    @classmethod
    def from_rule(cls, fields):
        _, field_2 = fields
        return cls(field_2)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_CRLF(self)


@dataclass
class NL:
    value: Any

    @classmethod
    def from_rule(cls, fields):
        value = fields
        return cls(value)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_NL(self)


@dataclass
class TEXTDATA:
    value: Any

    @classmethod
    def from_rule(cls, fields):
        value = fields
        return cls(value)

    def accept(self, visitor: "Visitor"):
        return visitor.visit_TEXTDATA(self)


class Visitor:
    def visit_file(self, node: file):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_file."
        )

    def visit_header(self, node: header):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_header."
        )

    def visit_record(self, node: record):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_record."
        )

    def visit_tail_record(self, node: tail_record):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_tail_record."
        )

    def visit_name(self, node: name):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_name."
        )

    def visit_tail_name(self, node: tail_name):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_tail_name."
        )

    def visit_field(self, node: field):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_field."
        )

    def visit_tail_field(self, node: tail_field):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_tail_field."
        )

    def visit_escaped(self, node: escaped):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_escaped."
        )

    def visit_non_escaped(self, node: non_escaped):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_non_escaped."
        )

    def visit_COMMA(self, node: COMMA):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_COMMA."
        )

    def visit_CR(self, node: CR):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_CR."
        )

    def visit_DQUOTE(self, node: DQUOTE):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_DQUOTE."
        )

    def visit_LF(self, node: LF):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_LF."
        )

    def visit_CRLF(self, node: CRLF):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_CRLF."
        )

    def visit_NL(self, node: NL):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_NL."
        )

    def visit_TEXTDATA(self, node: TEXTDATA):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement visit_TEXTDATA."
        )


class Parser(Combinators):
    @property
    def file(self):
        return self._file()

    def _file(self):
        return self.map(file.from_rule)(
            self.sequence(
                self.maybe(
                    self.sequence(
                        self.header,
                        self.NL,
                    )
                ),
                self.record,
                self.collect(self.zero_or_more((self.tail_record))),
                self.maybe(self.NL),
            )
        )

    @property
    def header(self):
        return self._header()

    def _header(self):
        return self.map(header.from_rule)(
            self.sequence(
                self.name,
                self.collect(self.zero_or_more((self.tail_name))),
            )
        )

    @property
    def record(self):
        return self._record()

    def _record(self):
        return self.map(record.from_rule)(
            self.sequence(
                self.field,
                self.collect(self.zero_or_more((self.tail_field))),
            )
        )

    @property
    def tail_record(self):
        return self._tail_record()

    def _tail_record(self):
        return self.map(tail_record.from_rule)(
            self.sequence(
                self.NL,
                self.record,
            )
        )

    @property
    def name(self):
        return self._name()

    def _name(self):
        return self.map(name.from_rule)(self.field)

    @property
    def tail_name(self):
        return self._tail_name()

    def _tail_name(self):
        return self.map(tail_name.from_rule)(
            self.sequence(
                self.COMMA,
                self.name,
            )
        )

    @property
    def field(self):
        return self._field()

    def _field(self):
        return self.map(field.from_rule)(
            self.choice(
                self.escaped,
                self.non_escaped,
            )
        )

    @property
    def tail_field(self):
        return self._tail_field()

    def _tail_field(self):
        return self.map(tail_field.from_rule)(
            self.sequence(
                self.COMMA,
                self.field,
            )
        )

    @property
    def escaped(self):
        return self._escaped()

    def _escaped(self):
        return self.map(escaped.from_rule)(
            self.sequence(
                self.DQUOTE,
                self.collect(
                    self.zero_or_more(
                        (
                            self.choice(
                                self.TEXTDATA,
                                self.COMMA,
                                self.CR,
                                self.LF,
                                self.sequence(
                                    self.DQUOTE,
                                    self.DQUOTE,
                                ),
                            )
                        )
                    )
                ),
                self.DQUOTE,
            )
        )

    @property
    def non_escaped(self):
        return self._non_escaped()

    def _non_escaped(self):
        return self.map(non_escaped.from_rule)(
            self.collect(self.zero_or_more((self.TEXTDATA)))
        )

    @property
    def COMMA(self):
        return self._COMMA()

    def _COMMA(self):
        return self.map(COMMA.from_rule)(self.regex("\\x2C"))

    @property
    def CR(self):
        return self._CR()

    def _CR(self):
        return self.map(CR.from_rule)(self.regex("\\x0D"))

    @property
    def DQUOTE(self):
        return self._DQUOTE()

    def _DQUOTE(self):
        return self.map(DQUOTE.from_rule)(self.regex("\\x22"))

    @property
    def LF(self):
        return self._LF()

    def _LF(self):
        return self.map(LF.from_rule)(self.regex("\\x0A"))

    @property
    def CRLF(self):
        return self._CRLF()

    def _CRLF(self):
        return self.map(CRLF.from_rule)(
            self.sequence(
                self.CR,
                self.LF,
            )
        )

    @property
    def NL(self):
        return self._NL()

    def _NL(self):
        return self.map(NL.from_rule)(
            self.choice(
                self.CRLF,
                self.LF,
            )
        )

    @property
    def TEXTDATA(self):
        return self._TEXTDATA()

    def _TEXTDATA(self):
        return self.map(TEXTDATA.from_rule)(
            self.choice(
                self.regex("[\\x20-\\x21]"),
                self.regex("[\\x23-\\x2B]"),
                self.regex("[\\x2D-\\x7E]"),
            )
        )


def parse(value: str):
    parser = Parser()
    f = next(parser.file(Stream.from_string(value)))
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

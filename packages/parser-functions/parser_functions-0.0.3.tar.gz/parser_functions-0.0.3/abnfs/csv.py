from dataclasses import dataclass
from typing import Any


@dataclass
class file:
    header: Any
    head_record: Any
    tail_records: Any

    @classmethod
    def from_rule(cls, fields):
        header, head_record, tail_records, _ = fields
        return cls(header, head_record, tail_records)


@dataclass
class tail_record:
    record: Any

    @classmethod
    def from_rule(cls, fields):
        _, record = fields
        return cls(record)


@dataclass
class header:
    head_name: Any
    tail_names: Any

    @classmethod
    def from_rule(cls, fields):
        head_name, tail_names = fields
        return cls(head_name, tail_names)


@dataclass
class tail_name:
    name: Any

    @classmethod
    def from_rule(cls, fields):
        _, name = fields
        return cls(name)


@dataclass
class record:
    head_field: Any
    tail_fields: Any

    @classmethod
    def from_rule(cls, fields):
        head_field, tail_fields = fields
        return cls(head_field, tail_fields)


@dataclass
class tail_field:
    field: Any

    @classmethod
    def from_rule(cls, fields):
        _, field = fields
        return cls(field)


@dataclass
class name:
    field: Any

    @classmethod
    def from_rule(cls, fields):
        field = fields
        return cls(field)


@dataclass
class field:
    value: Any

    @classmethod
    def from_rule(cls, fields):
        value = fields
        return cls(value)


@dataclass
class escaped:
    value: Any

    @classmethod
    def from_rule(cls, fields):
        _, value, _ = fields
        return cls(value)


@dataclass
class non_escaped:
    value: Any

    @classmethod
    def from_rule(cls, fields):
        value = fields
        return cls(value)


@dataclass
class COMMA:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()


@dataclass
class CR:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()


@dataclass
class DQUOTE:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()


@dataclass
class LF:

    @classmethod
    def from_rule(cls, fields):
        _ = fields
        return cls()


@dataclass
class CRLF:
    field_2: Any

    @classmethod
    def from_rule(cls, fields):
        _, field_2 = fields
        return cls(field_2)


@dataclass
class NL:
    value: Any

    @classmethod
    def from_rule(cls, fields):
        value = fields
        return cls(value)


@dataclass
class TEXTDATA:
    value: Any

    @classmethod
    def from_rule(cls, fields):
        value = fields
        return cls(value)


from parser_functions import Combinators, Stream


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
    def name(self):
        return self._name()

    def _name(self):
        return self.map(name.from_rule)(self.field)

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


def parse(path: str):
    with open(path, 'r', encoding='utf8') as f:
        data = f.read()
    parser = Parser()
    f = next(parser.file(Stream.from_string(data)))
    print(f.value)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Path to file to parse.')
    args = parser.parse_args()
    parse(args.path)


if __name__ == '__main__':
    main()

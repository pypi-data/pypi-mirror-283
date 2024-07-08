"""Module for parsing CSVs."""

from typing import Any, List

from parser_functions.combinators import Combinators, FailResult, ParserGen, Stream


class CSV(Combinators):
    """CSV file parsing combinators."""

    @property
    def comma(self) -> ParserGen:
        """Match a comma character."""
        return self.char(",")

    @property
    def line_end(self) -> ParserGen:
        """Match a line ending."""
        return self.choice(
            self.char("\n"),
            self.sequence(self.char("\r"), self.char("\n")),
        )

    @property
    def dq(self) -> ParserGen:
        """Match a double-quote character."""
        return self.char('"')

    @property
    def escaped_dq(self) -> ParserGen:
        """Match an escaped double-quote character.

        Inside a quoted CSV field "" is considered a ". This parser matches
        the double "" and replaces its value with a single ".
        """
        return self.map(lambda _: '"')(self.sequence(self.dq, self.dq))

    @property
    def unquoted_field(self) -> ParserGen:
        """Match an unquoted CSV field."""
        return self.join(
            self.collect(self.zero_or_more(self.all_except([",", '"', "\n", "\r"]))),
        )

    @property
    def quoted_field(self) -> ParserGen:
        """Match a quoted CSV field."""
        return self.join(
            self.sequence(
                self.dq,
                self.collect(
                    self.zero_or_more(
                        self.choice(
                            self.all_except(['"']),
                            self.escaped_dq,
                        )
                    )
                ),
                self.dq,
                flatten=True,
                take={1},
            )
        )

    @property
    def field(self) -> ParserGen:
        """Match a CSV field."""
        return self.choice(
            self.quoted_field,
            self.unquoted_field,
        )

    @property
    def record(self) -> ParserGen:
        """Match a CSV record."""
        return self.sequence(
            self.field,
            self.collect(
                self.zero_or_more(self.sequence(self.comma, self.field, take=1))
            ),
            flatten=True,
        )

    def _check_last_record(self, records):
        """Fix the last record.

        The last record can be [''] because a blank line with nothing on
        it is a valid CSV record and is collected. If this record exists it
        should be removed.
        """
        if records[-1] == [""]:
            return records[:-1]
        return records

    @property
    def records(self) -> ParserGen:
        """Match multiple CSV records."""
        return self.map(self._check_last_record)(
            self.sequence(
                self.sequence(self.record),
                self.collect(
                    self.zero_or_more(self.sequence(self.line_end, self.record, take=1))
                ),
                self.maybe(self.line_end),
                take=[0, 1],
                flatten=True,
            )
        )

    def loads(self, string: str, header=True) -> List[Any]:
        """Load a CSV string into a list of dictionaries.

        If header is False, each row is loaded independently. The final return
        value will be a list of lists.

        If header is True the first record, the header, will be used as keys for
        a dictionary. Each following row is a set of values. The finaly return value
        will be a list of dictionaries.

        For example:
        ```
        a,b,c
        1,2,3
        4,5,6
        ```

        With `header = True` will load as:

            [{'a': '1', 'b': '2', 'c': '3'}, {'a': '4', 'b': '5', 'c': '6'}]

        With `header = False` will load as:

            [['a', 'b', 'c'], ['1', '2', '3'], ['4', '5', '6']]
        """
        result: List[Any] = []
        records = next(self.records(Stream.from_string(string)))
        match records:
            case FailResult():
                raise ValueError("Parse error")
        for i, record in enumerate(records.value):
            if header is True:
                header = record
            elif header:
                if len(header) != len(record):
                    raise ValueError(
                        f"Record {i} length ({len(record)}) does "
                        f"not match header length ({len(header)})."
                    )
                result.append(dict(zip(header, record)))
            else:
                result.append(record)
        return result

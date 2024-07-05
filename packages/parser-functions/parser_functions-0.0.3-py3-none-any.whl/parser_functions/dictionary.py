from typing import Any, Dict

from parser_functions.combinators import (
    Combinators,
    FailResult,
    ParserGen,
    Stream,
    SuccessResult,
)


class Dictionary(Combinators):
    """Class containing combinators for parsing dictionaries."""

    @property
    def colon(self) -> ParserGen:
        """Match a colon character."""
        return self.token(self.char(":"))

    @property
    def comma(self) -> ParserGen:
        """Match a comma character."""
        return self.token(self.char(","))

    @property
    def l_bracket(self) -> ParserGen:
        """Match a left bracket character."""
        return self.token(self.char("{"))

    @property
    def r_bracket(self) -> ParserGen:
        """Match a right bracket character."""
        return self.token(self.char("}"))

    @property
    def l_brace(self) -> ParserGen:
        """Match a left brace character."""
        return self.token(self.char("["))

    @property
    def r_brace(self) -> ParserGen:
        """Match a right brace character."""
        return self.token(self.char("]"))

    @property
    def s_quote(self) -> ParserGen:
        """Match a single quote character."""
        return self.char("'")

    @property
    def d_quote(self) -> ParserGen:
        """Match a double quote character."""
        return self.char('"')

    @property
    def key(self) -> ParserGen:
        """Match a dictionary key."""
        return self.token(
            self.choice(
                self.letters,
                self.string,
            )
        )

    @property
    def dict_boolean(self) -> ParserGen:
        """Match a bool value."""
        bools = {
            'TRUE': True,
            'True': True,
            'true': True,
            'FALSE': False,
            'False': False,
            'false': False,
        }
        return self.map(bools.get)(
            self.choice(*[self.token(self.word(opt)) for opt in bools])
        )

    @property
    def escaped_dq(self):
        return self.replace('"')(self.sequence(self.char('\\'), self.char('"')))

    @property
    def escaped_sq(self):
        return self.replace("'")(self.sequence(self.char('\\'), self.char("'")))

    @property
    def escaped_backslash(self):
        return self.replace('\\')(self.sequence(self.char('\\'), self.char('\\')))

    @property
    def escaped_newline(self):
        return self.replace('\n')(self.sequence(self.char('\\'), self.char('n')))

    @property
    def escaped_linefeed(self):
        return self.replace('\r')(self.sequence(self.char('\\'), self.char('r')))

    @property
    def str_chars(self) -> ParserGen:
        """Match allowed string characters."""
        return self.choice(
            self.all_except(['"', "'", '\\', '\n', '\r']),
            self.escaped_backslash,
            self.escaped_linefeed,
            self.escaped_newline,
        )

    @property
    def dq_string(self) -> ParserGen:
        """Match a double quoted string."""
        return self.join(
            self.sequence(
                self.d_quote,
                self.collect(
                    self.zero_or_more(
                        self.choice(
                            self.str_chars,
                            self.escaped_dq,
                            self.s_quote,
                        )
                    )
                ),
                self.d_quote,
                take=1,
            )
        )

    @property
    def sq_string(self) -> ParserGen:
        """Match a double quoted string."""
        return self.join(
            self.sequence(
                self.s_quote,
                self.collect(
                    self.zero_or_more(
                        self.choice(
                            self.str_chars,
                            self.escaped_sq,
                            self.d_quote,
                        )
                    )
                ),
                self.s_quote,
                take=1,
            )
        )

    @property
    def string(self) -> ParserGen:
        """Match a string."""
        return self.token(
            self.choice(
                self.sq_string,
                self.dq_string,
            )
        )

    @property
    def number(self) -> ParserGen:
        return self.token(super().number)

    @property
    def scalar(self) -> ParserGen:
        """Match a scalar value."""
        return self.choice(
            self.dict_boolean,
            self.number,
            self.string,
        )

    @property
    def list_element(self):
        return self.sequence(self.value, self.maybe(self.comma), take=0)

    def _list(self) -> ParserGen:
        return self.sequence(
            self.l_brace,
            self.collect(self.zero_or_more(self.list_element)),
            self.r_brace,
            take=1,
        )

    @property
    def value(self) -> ParserGen:
        """Match a dictionary value."""
        return self.choice(
            self.scalar,
            self.defer(self._list),
            self.defer(self._dictionary),
        )

    @property
    def kv_pair(self) -> ParserGen:
        """Match a key-value pair."""
        return self.sequence(
            self.key,
            self.colon,
            self.value,
            self.maybe(self.comma),
            take=[0, 2],
        )

    def _dictionary(self) -> ParserGen:
        return self.map(dict)(
            self.sequence(
                self.l_bracket,
                self.collect(self.zero_or_more(self.kv_pair)),
                self.r_bracket,
                take=1,
            )
        )

    @property
    def dictionary(self) -> ParserGen:
        """Match a dictionary.

        Tries to build a python dictionary with fairly permissive rules.
        """
        return self._dictionary()

    def loads(self, string: str) -> Dict[str, Any]:
        match next(self.dictionary(Stream.from_string(string))):
            case SuccessResult(d, _):
                return d
            case FailResult(s):
                raise ValueError(f"Parse error {s}")

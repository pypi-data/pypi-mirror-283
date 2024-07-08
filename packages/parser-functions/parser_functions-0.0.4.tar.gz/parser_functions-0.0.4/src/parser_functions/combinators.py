import re
import sys
from dataclasses import dataclass
from typing import Any, Callable, Generator, Generic, List, TypeAlias, TypeVar

T = TypeVar("T")


def primed_generator(fn):
    """Create a generator and call next once.

    Used on generators that have a yield statement right away. The execution
    is then frozen just past the first yield statement. This method lets us
    create a generator, and return it in a partially executed state for some
    other consumer to call next() without having to first create the generator
    by calling the method that created it.

    Is particularly useful when returning a generator that depends on another
    generator. We don't want to call next() on the dependency generator until
    the dependent generator has next() called on it.
    """
    gen = fn()
    next(gen)
    return gen


@dataclass
class SuccessResult(Generic[T]):
    """Class representing a successful result."""

    value: T
    stream: "Stream"

    def __bool__(self):
        """Return True to indicate success."""
        return True


@dataclass
class FailResult:
    """Class representing a failed result."""

    stream: "Stream"
    reason: str = ""

    def __bool__(self):
        """Return False to indicate failure."""
        return False

    def _space_since_last_newline(self):
        i = self.stream.idx
        while i >= 0 and self.stream.data[i] != '\n':
            i -= 1
        return self.stream.idx - i

    def _cutout_line(self):
        i, j = self.stream.idx, self.stream.idx
        while i >= 0 and self.stream.data[i] != '\n':
            i -= 1
        while j < len(self.stream.data) and self.stream.data[j]:
            j += 1
        return self.stream.data[i:j]

    def __repr__(self) -> str:
        lines = [
            ''.join(self._cutout_line()),
            (' ' * self._space_since_last_newline()) + '^',
            self.reason,
        ]
        return '\n'.join(lines)


Result: TypeAlias = SuccessResult | FailResult
ResultGen: TypeAlias = Generator[Result, None, None]


@dataclass
class Stream(Generic[T]):
    """Class representing a stream of data."""

    data: List[T] | str
    idx: int = 0

    def consume(self) -> "Stream":
        """Consume the next item in the stream."""
        return Stream(self.data, self.idx + 1)

    @property
    def value(self) -> T | str:
        """Get the current value in the stream."""
        return self.data[self.idx]

    @classmethod
    def from_string(cls, string: str) -> "Stream[str]":
        """Create a stream from a string."""
        return Stream(string, 0)


Parser: TypeAlias = Callable[[Stream], Result]
ParserGen: TypeAlias = Callable[[Stream], ResultGen]


class Combinators:
    """Class containing various combinator methods for parsing."""

    def shift(self, stream: Stream) -> ResultGen:
        """Shift the stream by one position if possible."""
        if stream.idx >= len(stream.data):
            yield FailResult(stream)
        yield SuccessResult(stream.value, stream.consume())

    def nothing(self, stream: Stream) -> ResultGen:
        """Return a successful result with None value."""
        yield SuccessResult(None, stream)

    def filter(
        self, predicate: Callable[[T], bool]
    ) -> Callable[[ParserGen], ParserGen]:
        """Filter the results of a parser based on a predicate."""

        def wrapper(parser: ParserGen) -> ParserGen:
            def parse(stream: Stream) -> ResultGen:
                def lazy_filter():
                    yield
                    match m := next(parser(stream)):
                        case SuccessResult(value, s):
                            yield m if predicate(value) else FailResult(s)
                        case _:
                            yield m

                return primed_generator(lazy_filter)

            return parse

        return wrapper

    def literal(self, expected: T) -> Callable[[ParserGen], ParserGen]:
        """Match a literal value in the stream."""
        return self.filter(lambda v: v == expected)

    def char(self, expected: T) -> ParserGen:
        """Match a specific character in the stream."""
        return self.literal(expected)(self.shift)

    def word(self, expected: str) -> ParserGen:
        """Match a specific sequence of characters."""
        return self.join(self.sequence(*[self.char(letter) for letter in expected]))

    def regex(self, regex) -> ParserGen:
        """Match a regular expression in the stream."""
        if isinstance(regex, str):
            regex = re.compile(regex)
        return self.filter(regex.match)(self.shift)

    def all_except(self, values: List[str]) -> ParserGen:
        """Match any character except the specified values."""
        return self.regex(re.compile(f'[^{"".join(values)}]'))

    def map(self, mapping: Callable[[T], Any]) -> Callable[[ParserGen], ParserGen]:
        """Map the result of a parser using a mapping function."""

        def wrapper(parser: ParserGen) -> ParserGen:
            def parse(stream: Stream) -> ResultGen:
                def lazy_map():
                    yield
                    match m := next(parser(stream)):
                        case SuccessResult(value, next_stream):
                            yield SuccessResult(mapping(value), next_stream)
                        case _:
                            yield m

                return primed_generator(lazy_map)

            return parse

        return wrapper

    def spy(self, msg: str) -> Callable[[ParserGen], ParserGen]:
        """Inject a print statement after a Parser to spy on its result value."""

        def _spy(target):
            sys.stderr.write(msg.format(target))
            return target

        return self.map(_spy)

    @property
    def join(self):
        """Join a list into one value.

        This is essentially a sugar for map(''.join) with some extra
        logic for handling None. The maybe combinator can spit out None
        values into our stream which ''.join cannot handle.

        Also handles the case where you have [value, [value], [value]] as
        the result of the form:

            sequence(
                value,
                zero_or_more(sequence(value, whitespace)),
            )

        The final output you want is in the form [value, value, value].
        """

        def joining(x):
            lists = [
                (lst if isinstance(lst, list) else [lst])
                for lst in x
                if lst is not None
            ]
            final = "".join([v for lst in lists for v in lst])
            return final

        return self.map(joining)

    def replace(self, replacement: Any) -> Callable[[ParserGen], ParserGen]:
        """Replace the next parser result with the value of replacement."""
        return self.map(lambda _: replacement)

    def defer(self, deferred, *dargs, **dkwargs):
        """Defer the execution of a parser.

        This is useful for self-recursive grammars. Defer can be used to prevent
        a child function from referring up to its parent function creating an
        infinite loop at runtime.

        For example
        ```
        class Dictionary:
            ...
            @property
            def key(self) -> ParserGen:
                return self.token(self.letters)

            @property
            def value(self) -> ParserGen:
                return self.choice(
                    self.token(self.letters),
                    self.defer(self._dictionary),
                )

            @property
            def kv_pair(self) -> ParserGen:
                return self.sequence(
                    self.left(self.key, self.colon),
                    self.left(self.value, self.maybe(self.comma)),
                )

            def _dictionary(self) -> ParserGen:
                return self.map(dict)(self.nth(
                    1,
                    self.l_bracket,
                    self.collect(self.zero_or_more(self.kv_pair)),
                    self.r_bracket,
                ))

            @property
            def dictionary(self) -> ParserGen:
                return self._dictionary()
        ```

        The value of a key/value pair in a dictionary can contain another dictionary.
        Since these are function combinators this will cause an infinite loop when
        trying run this definition without the defer.

        Wrapping the self._dictionary  choice in an defer() means that it will not be
        evaluated up front. Instead it will be evaluated only if we acutally reach that
        branch of the choice() while parsing.
        """

        def inner(*args, **kwargs):
            return deferred(*dargs, **dkwargs)(*args, **kwargs)

        return inner

    def either(self, left: ParserGen, right: ParserGen) -> ParserGen:
        """Combine two parsers and return the result of the first successful one."""

        def parser(stream: Stream) -> ResultGen:
            if isinstance(left, str):
                print(left, right)
            yield next(left(stream)) or next(right(stream))

        return parser

    def maybe(self, parser: ParserGen) -> ParserGen:
        """Make a parser optional.

        Returns None if it was not matched.
        """
        return self.either(parser, self.nothing)

    def choice(self, parser: ParserGen, *parsers: ParserGen) -> ParserGen:
        """Combine multiple parsers and return the result of the first successful one.

        Importantly, later parsers in the list are not invoked if an earlier parser is
        successful.
        """
        return self.either(parser, self.choice(*parsers)) if parsers else parser

    def _sequence_update_results(self, results, i, value, flatten, take):
        if take:
            if isinstance(take, int):
                # If take is an int we are only taking a single nth value.
                if i == take:
                    results.append(value)
                return
            if i not in take:
                return

        if isinstance(value, list) and flatten:
            results.extend(value)
        else:
            results.append(value)

    def sequence(self, *parsers: ParserGen, flatten=False, take=None) -> ParserGen:
        """Combine multiple parsers in sequence.

        If any parser fails the overall parse is a failure.
        """

        def _single_result():
            return isinstance(take, int)

        def parser(stream: Stream):
            def lazy_sequence():
                nonlocal stream
                yield
                results = []
                for i, p in enumerate(parsers):
                    match m := next(p(stream)):
                        case SuccessResult(value, new_stream):
                            self._sequence_update_results(
                                results, i, value, flatten, take
                            )
                            stream = new_stream
                        case _:
                            yield m
                yield SuccessResult(results[0] if _single_result() else results, stream)

            return primed_generator(lazy_sequence)

        return parser

    def one_or_more(self, target: ParserGen) -> ParserGen:
        """Match one or more occurrences of a parser."""

        def parser(stream: Stream) -> ResultGen:
            def lazy_one_or_more():
                nonlocal stream
                returned = False
                yield
                while True:
                    match m := next(target(stream)):
                        case SuccessResult(_, s):
                            yield m
                            returned = True
                            stream = s
                        case _:
                            if not returned:
                                yield m
                            break

            return primed_generator(lazy_one_or_more)

        return parser

    def zero_or_more(self, target: ParserGen) -> ParserGen:
        """Match zero or more occurrences of a parser.

        Yields None when zero are matched.
        """

        def parser(stream: Stream) -> ResultGen:
            def lazy_zero_or_more():
                nonlocal stream
                returned = False
                yield
                while True:
                    match m := next(target(stream)):
                        case SuccessResult(_, new_stream):
                            yield m
                            returned = True
                            stream = new_stream
                        case _:
                            if not returned:
                                yield SuccessResult(None, stream)
                            break

            return primed_generator(lazy_zero_or_more)

        return parser

    def collect(self, or_more: ParserGen, filter_none=True) -> ParserGen:
        """Resolves a zero_or_more or one_or_more and hoists results to an array."""

        def parser(stream: Stream) -> ResultGen:
            results = []
            for r in or_more(stream):
                match r:
                    case SuccessResult(v, s):
                        if filter_none and v is not None:
                            results.append(v)
                        stream = s
                    case _:
                        yield r
            yield SuccessResult(results, stream)

        return parser

    def repeat(self, n: int):
        """Repeat a parser n times."""

        def wrapper(parser: ParserGen) -> ParserGen:
            return self.sequence(*[parser for _ in range(n)])

        return wrapper

    @property
    def letter(self) -> ParserGen:
        """Match a letter character."""
        return self.filter(str.isalpha)(self.shift)

    @property
    def letters(self) -> ParserGen:
        """Match one or more letter characters."""
        return self.map("".join)(self.collect(self.one_or_more(self.letter)))

    @property
    def whitespace(self) -> ParserGen:
        """Match zero or more whitespace characters."""
        return self.collect(self.zero_or_more(self.filter(str.isspace)(self.shift)))

    def token(self, target: ParserGen) -> ParserGen:
        """Match a parser preceded by optional whitespace.

        Only the parsers result is returned, the whitespace is ignored.
        """
        return self.sequence(self.whitespace, target, take=1)

    @property
    def digit(self) -> ParserGen:
        """Match a digit character."""
        return self.filter(str.isnumeric)(self.shift)

    @property
    def digits(self) -> ParserGen:
        """Match one or more digit characters."""
        return self.map("".join)(self.collect(self.one_or_more(self.digit)))

    @property
    def dot(self) -> ParserGen:
        """Match a dot character."""
        return self.char(".")

    @property
    def decimal_digits(self) -> ParserGen:
        """Match a sequence of decimal digits."""
        return self.map("".join)(
            self.sequence(
                self.digits,
                self.dot,
                self.digits,
            )
        )

    @property
    def decimal(self) -> ParserGen:
        """Match a decimal number.

        Casts the result to a float.
        """
        return self.map(float)(self.decimal_digits)

    @property
    def integer(self) -> ParserGen:
        """Match an integer number.

        Casts the result to an int"""
        return self.map(int)(self.digits)

    @property
    def float(self) -> ParserGen:
        """Match a float number.

        Casts the result to a float.
        """
        return self.either(self.decimal, self.map(float)(self.digits))

    @property
    def number(self) -> ParserGen:
        """Match an integer or float number.

        Casts the result to a int if it can, otherwise float.
        """
        return self.either(self.decimal, self.integer)


c = Combinators()


def add_spy(function):
    """Decorator to add a spy parser automatically based on function name"""

    def wrapper(*args, **kwargs):
        message = f'{function.__name__}: {{}}\n'
        result = function(*args, **kwargs)
        return c.spy(message)(result)

    return wrapper

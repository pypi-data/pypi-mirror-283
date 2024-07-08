"""ABNF parser Combinator class.

Generates a tree of ASTNodes.
"""

from parser_functions import Combinators
from parser_functions.abnf.ast import (
    AlternationNode,
    CharValNode,
    ConcatenationNode,
    GroupNode,
    HexNode,
    OptionNode,
    RepititionNode,
    RuleListNode,
    RuleNameNode,
    RuleNode,
)
from parser_functions.combinators import add_spy


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
    def vchar_without_dquote(self):
        """Match visible character except dqoute"""
        return self.regex('[\x21-\x21\x23-\x7e]')

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
    def br(self):
        """Match line break followed by whitespace"""
        return self.sequence(
            self.maybe(self.sp),
            self.choice(self.comment, self.nl),
            self.maybe(self.ws),
            take=1,
        )


class ABNF(ABNFCore):

    @property
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
                take=[0, 2],
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
                self.maybe(self.repeat_config),
                self.element,
            )
        )

    @property
    def repeat_config(self):
        return self.choice(
            self.sequence(
                self.maybe(self.digits),
                self.char('*'),
                self.maybe(self.digits),
                take=[0, 2],
            ),
            self.digits,
        )

    @property
    def element(self):
        return self.choice(
            self.rulename,
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

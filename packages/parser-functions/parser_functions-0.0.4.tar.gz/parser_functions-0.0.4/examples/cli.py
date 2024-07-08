import sys
from dataclasses import dataclass, field
from typing import Any, Callable, List, TypeAlias

from parser_functions import Combinators, Stream

ArgType: TypeAlias = bool | str


@dataclass
class Argument(Combinators):
    name: str
    typ: ArgType

    def rule(self):
        return self.sequence(self.word(f'--{self.name}'))


@dataclass
class Command(Combinators):
    name: str
    fn: Callable[[Any], Any]
    args: List[Argument] = field(default_factory=list)

    def add_argument(self, term, typ: ArgType):
        arg = Argument(term, typ)
        self.args.append(arg)
        return arg

    def rule(self):
        return self.sequence(
            self.word(self.name),
        )


def search(term):
    print(term)


@dataclass
class CLI(Combinators):

    commands: List[Command] = field(default_factory=list)

    def add_command(self, command: str, fn) -> Command:
        cmd = Command(command, fn)
        self.commands.append(cmd)
        return cmd

    # def parse(self, string: str):
    #     stream = Stream.from_string(string)
    #     options = self.choice(*[self.word(cmd.name) for cmd in self.commands])
    #     fn_mapping = {
    #         cmd.name: cmd.fn for cmd in self.commands
    #     }
    #     r = next(self.apply(fn_mapping)(self.sequence(options))(stream))
    #     print(r)

    def command(self, command, *args):
        self.sequence(
            self.token(self.word(command)), self.choice(*args) if args else self.nothing
        )

    def cli(self, *commands):
        return self.apply(
            {
                'search': search,
            }
        )(self.choice(*commands))

    def parse(self, string):
        next(
            self.cli(
                self.command('search'),
                self.command('destroy'),
            )(Stream.from_string(string))
        )

    # def parse(self, string):
    #     return next(self.apply({
    #         'search': search
    #     })(self.choice(
    #         self.sequence(
    #             self.token(self.word('search')),
    #             self.collect(self.zero_or_more(
    #                 self.choice(
    #                     self.sequence(self.token(self.word('--term')), self.token(self.letters), take=1),
    #                     self.token(self.word('hello')),
    #                 )
    #             )),
    #             flatten=True,
    #         ),
    #     ))(Stream.from_string(string)))


def main():
    cli = CLI()
    # search_cmd = cli.add_command('search', search)
    # search_cmd.add_argument('--term', 'bool')
    # cli.add_command('destroy', lambda: print("destroy"))
    r = cli.parse(' '.join(sys.argv[1:]) if len(sys.argv) > 1 else "")
    print(r)


if __name__ == "__main__":
    main()

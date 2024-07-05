"""Command line tool for generating parsers from ABNF files."""

import argparse

from parser_functions.abnf import ABNF, ParserFileGenerator
from parser_functions.combinators import Stream


def parse(path: str):
    with open(path, 'r', encoding='utf8') as f:
        data = f.read()

    abnf = ABNF()
    ast = next(abnf.rulelist(Stream.from_string(data))).value
    gen = ParserFileGenerator(file_data=data)
    gen.generate(ast)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', help='Path to ABNF grammar file.')
    args = parser.parse_args()
    parse(args.path)


if __name__ == "__main__":
    main()

from parser_functions.combinators import FailResult, Stream, SuccessResult

from .permissive_parser import Parser as PermissiveParser
from .permissive_visitor import JSONVisitor as PermissiveJSONVisitor
from .strict_parser import Parser as StrictParser
from .strict_visitor import JSONVisitor as StrictJSONVisitor


def loads(value: str, strict=True):
    if strict:
        parser, visitor = StrictParser(), StrictJSONVisitor()
    else:
        parser, visitor = PermissiveParser(), PermissiveJSONVisitor()
    r = next(parser.json_text(Stream.from_string(value)))
    match r:
        case SuccessResult(
            v,
        ):
            return v.accept(visitor)
        case FailResult(s):
            raise ValueError(f'Could not parse: {s}')

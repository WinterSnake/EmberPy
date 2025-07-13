#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
import sys
from collections.abc import Sequence
from pathlib import Path
from .errors import DebugLevel, EmberError
from .frontend import Lexer, Parser, Token
from .middleware.nodes import Node

## Constants
LEXER_LEVEL: DebugLevel = DebugLevel.Trace
PARSER_LEVEL: DebugLevel = DebugLevel.Trace


## Functions
def _entry() -> None:
    source: Path = Path("tests/00-operations.ember")
    output = parse_source(source)
    if isinstance(output, Sequence):
        for err in output:
            print(err.message, file=sys.stderr)
        sys.exit(1)


def parse_source(source: Path) -> Node | Sequence[EmberError]:
    """Lex and parse a source file and return parsed AST or found errors"""
    global LEXER_LEVEL, PARSER_LEVEL
    lexer: Lexer = Lexer(source)
    lexer.debug_level = LEXER_LEVEL
    parser: Parser = Parser(lexer.lex())
    parser.debug_level = PARSER_LEVEL
    ast = parser.parse()
    errors = tuple((*lexer.errors, *parser.errors))
    return errors if errors else ast


def usage() -> None:
    print("emberc <file.ember>")


## Body
if __name__ == "__main__":
    _entry()

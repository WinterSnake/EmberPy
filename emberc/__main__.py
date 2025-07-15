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
from .middleware.symbol_table import SymbolTable
from .middleware.interpreter import Interpreter

## Constants
LEXER_LEVEL: DebugLevel = DebugLevel.Off
PARSER_LEVEL: DebugLevel = DebugLevel.Off


## Functions
def _entry() -> None:
    if len(sys.argv) < 2:
        print("No source file provided", file=sys.stderr)
        usage()
        return
    table = SymbolTable()
    source: Path = Path(sys.argv[1])
    output = parse_source(source, table)
    if isinstance(output, Sequence):
        for err in output:
            print(err.message, file=sys.stderr)
        sys.exit(64)
    print(table.entries)
    Interpreter.run(output, table, DebugLevel.Off)


def parse_source(
    source: Path, table: SymbolTable
) -> Node | Sequence[EmberError]:
    """Lex and parse a source file and return parsed AST or found errors"""
    global LEXER_LEVEL, PARSER_LEVEL
    lexer: Lexer = Lexer(source)
    lexer.debug_level = LEXER_LEVEL
    parser: Parser = Parser(lexer.lex())
    parser.debug_level = PARSER_LEVEL
    ast = parser.parse(table)
    errors = tuple((*lexer.errors, *parser.errors))
    return errors if errors else ast


def usage() -> None:
    print("emberc <file.ember>")


## Body
if __name__ == "__main__":
    _entry()

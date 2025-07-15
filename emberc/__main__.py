#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
import sys
from collections.abc import Sequence
from pathlib import Path
from .errors import EmberError
from .frontend import Lexer, Parser, Token
from .middleware.nodes import Node
from .middleware.symbol_table import SymbolTable
from .middleware.walkers import InterpreterWalker, PrinterWalker


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
    PrinterWalker.run(output)
    InterpreterWalker.run(output, table)


def parse_source(
    source: Path, table: SymbolTable
) -> Node | Sequence[EmberError]:
    """Lex and parse a source file and return parsed AST or found errors"""
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer.lex())
    ast = parser.parse(table)
    errors = tuple((*lexer.errors, *parser.errors))
    return errors if errors else ast


def usage() -> None:
    print("emberc <file.ember>")


## Body
if __name__ == "__main__":
    _entry()

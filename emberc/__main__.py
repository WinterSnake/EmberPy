#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
import sys
from pathlib import Path
from .frontend import Lexer, Parser, Token
from .middleware.interpreter import InterpreterVisitor


## Functions
def _entry() -> None:
    if len(sys.argv) != 2:
        print("No source file provided", file=sys.stderr)
        usage()
        return
    source = Path(sys.argv[1])
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer.lex())
    ast = parser.parse()
    InterpreterVisitor.run(ast)


def usage() -> None:
    print("emberc <file.ember>")


## Body
if __name__ == "__main__":
    _entry()

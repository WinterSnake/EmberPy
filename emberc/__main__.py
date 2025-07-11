#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
import sys
from collections.abc import Iterator
from pathlib import Path
from .frontend import Lexer, Parser, Token
from .middleware.interpreter import InterpreterVisitor

## Constants
DEBUG_MODE: bool = False
DUMP_TOKENS: bool = False


## Functions
def _entry() -> None:
    global DEBUG_MODE, DUMP_TOKENS
    if len(sys.argv) < 2:
        print("No source file provided", file=sys.stderr)
        usage()
        return
    source: Path | None = None
    for arg in sys.argv[1:]:
        if arg in ("-t", "--dump-tokens"):
            DUMP_TOKENS = True
        elif arg in ("-d", "--debug-mode"):
            DEBUG_MODE = True
        else:
            source = Path(arg)
    if source is None:
        print("No source file provided", file=sys.stderr)
        usage()
        return
    lexer: Lexer = Lexer(source)
    token_iter: Iterator[Token] = lexer.lex()
    if DUMP_TOKENS:
        tokens = [token for token in token_iter]
        for token in tokens:
            print(token)
        token_iter = iter(tokens)
    parser: Parser = Parser(token_iter, DEBUG_MODE)
    ast = parser.parse()
    InterpreterVisitor.run(ast, DEBUG_MODE)


def usage() -> None:
    print("emberc [options] <file.ember>")
    print("\t-t, --dump-tokens: print out all found tokens from given source file")


## Body
if __name__ == "__main__":
    _entry()

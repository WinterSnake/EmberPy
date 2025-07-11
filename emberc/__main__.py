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

## Constants
DUMP_TOKENS: bool = False


## Functions
def _entry() -> None:
    global DUMP_TOKENS
    if len(sys.argv) < 2:
        print("No source file provided", file=sys.stderr)
        usage()
        return
    source: Path | None = None
    for arg in sys.argv[1:]:
        if arg in ("-t", "--dump-tokens"):
            DUMP_TOKENS = True
        else:
            source = Path(arg)
    if source is None:
        print("No source file provided", file=sys.stderr)
        usage()
        return
    lexer: Lexer = Lexer(source)
    token_iter = lexer.lex()
    if DUMP_TOKENS:
        tokens = [token for token in token_iter]
        for token in tokens:
            print(token)
        token_iter = iter(tokens)
    parser: Parser = Parser(token_iter)
    ast = parser.parse()
    return
    InterpreterVisitor.run(ast)


def usage() -> None:
    print("emberc <file.ember>")


## Body
if __name__ == "__main__":
    _entry()

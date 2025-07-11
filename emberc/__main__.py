#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
from pathlib import Path
from .frontend import Lexer, Parser, Token
from .middleware.interpreter import InterpreterVisitor


## Functions
def _entry() -> None:
    file: Path = Path("./tests/00-operators.ember")
    lexer: Lexer = Lexer(file)
    tokens: list[Token] = [token for token in lexer.lex()]
    #for token in tokens:
    #    print(token)
    parser: Parser = Parser(iter(tokens))
    ast = parser.parse()
    InterpreterVisitor.run(ast)


## Body
if __name__ == "__main__":
    _entry()

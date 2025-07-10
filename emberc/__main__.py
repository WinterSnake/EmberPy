#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
from pathlib import Path
from .frontend import Lexer, Token


## Functions
def _entry() -> None:
    file: Path = Path("./tests/00-operators.ember")
    lexer: Lexer = Lexer(file)
    tokens: list[Token] = [token for token in lexer.lex()]
    for token in tokens:
        print(token)


## Body
if __name__ == "__main__":
    _entry()

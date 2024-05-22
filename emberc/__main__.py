#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
import sys
from pathlib import Path
from .frontend import Node, Token, lex, parse
from .backend import interpret

## Constants
source = Path("./tests/operators.ember")

## Body
tokens: list[Token] = lex(source)
ast: list[Node] | None = parse(tokens)
if ast is None:
    sys.exit(1)
interpret(ast)

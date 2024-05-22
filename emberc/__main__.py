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
source = Path("./tests/variables.ember")
PRINT_TOKENS: bool = False
PRINT_AST: bool = True

## Body
tokens: list[Token] = lex(source)
if PRINT_TOKENS:
    for token in tokens:
        print(token)
ast: list[Node] | None = parse(tokens)
if ast is None:
    sys.exit(1)
if PRINT_AST:
    for node in ast:
        print(node)
interpret(ast)

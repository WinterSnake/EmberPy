#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
import sys
from pathlib import Path
from .frontend import Node, Token, lex, parse

## Constants
source = Path("./tests/lexing.ember")

## Body
tokens: list[Token] = lex(source)
for token in tokens:
    print(token)
node: Node = parse(tokens)
print(node)

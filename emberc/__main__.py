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
source = Path("./tests/operators.ember")

## Body
tokens: list[Token] = lex(source)
ast: Node = parse(tokens)
for node in ast:
    print(node)

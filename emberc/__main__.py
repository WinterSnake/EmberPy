#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
import sys
from pathlib import Path
from typing import Type
from .frontend import Node, Token, lex, parse
from .backend import NodeVisitor, FoldingOptimizationPass, interpret

## Constants
source = Path("./tests/variables.ember")
PRINT_TOKENS: bool = False
PRINT_AST: bool = True
PASSES: list[Type[NodeVisitor]] = [FoldingOptimizationPass]

## Body
tokens: list[Token] = lex(source)
if PRINT_TOKENS:
    for token in tokens:
        print(token)
ast: list[Node] | None = parse(tokens)
if ast is None:
    sys.exit(1)
for _pass in PASSES:
    pass_instance = _pass()
    for i, node in enumerate(ast):
        ast[i] = node.visit(pass_instance)
if PRINT_AST:
    for node in ast:
        print(node)
interpret(ast)

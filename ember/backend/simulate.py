#!/usr/bin/python
##-------------------------------##
## Ember: Backend                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Simulate                      ##
##-------------------------------##

## Imports
from typing import Any


## Functions
def simulate_ast(ast: Any) -> Any:
    """Simulate an ast through python"""
    if isinstance(ast, int):
        return ast
    elif isinstance(ast, dict):
        op: str = list(ast.keys())[0]
        lhs: Any = simulate_ast(ast[op]['lhs'])
        rhs: Any = simulate_ast(ast[op]['rhs'])
        if op == '+':
            return lhs + rhs
        elif op == '-':
            return lhs - rhs
        elif op == '*':
            return lhs * rhs
        elif op == '/':
            return lhs // rhs
        elif op == '%':
            return lhs % rhs

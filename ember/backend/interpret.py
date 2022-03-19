#!/usr/bin/python
##-------------------------------##
## Ember: Backend                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Interpret                     ##
##-------------------------------##

## Imports
from typing import Any


## Functions
def interpret_ast(nodes: list[Any]) -> int:
    """Interpret an ast"""
    for node in nodes:
        result: int = _interpret_node(node)
    return result


def _interpret_node(node: Any) -> Any:
    """Interpret a single node"""
    if isinstance(node, int):
        return node
    elif isinstance(node, dict):
        op: str = list(node.keys())[0]
        lhs: Any = _interpret_node(node[op]['lhs'])
        rhs: Any = _interpret_node(node[op]['rhs'])
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

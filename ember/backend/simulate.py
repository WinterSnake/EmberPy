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
def simulate_ast(nodes: list[Any]) -> int:
    """Simulate an ast through python"""
    for node in nodes:
        result: int = _simulate_node(node)
    return result


def _simulate_node(node: Any) -> Any:
    """Simulate a single node through python"""
    if isinstance(node, int):
        return node
    elif isinstance(node, dict):
        op: str = list(node.keys())[0]
        lhs: Any = _simulate_node(node[op]['lhs'])
        rhs: Any = _simulate_node(node[op]['rhs'])
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

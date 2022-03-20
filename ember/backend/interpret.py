#!/usr/bin/python
##-------------------------------##
## Ember: Backend                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Interpret                     ##
##-------------------------------##

## Imports
from typing import Any

from frontend.lexer import Token


## Functions
def interpret_ast(nodes: list[Any]) -> int:
    """Interpret an ast"""
    for node in nodes:
        result: int = _interpret_node(node)
    return 0
 

def _interpret_node(node: Any) -> Any:
    """Interpret a single node"""
    if isinstance(node, int):
        return node
    elif isinstance(node, dict):
        op: str = list(node.keys())[0]
        if op in (
            Token.TYPE.ADD, Token.TYPE.SUB, Token.TYPE.MUL,
            Token.TYPE.DIV, Token.TYPE.MOD
        ):
            lhs: Any = _interpret_node(node[op]['lhs'])
            rhs: Any = _interpret_node(node[op]['rhs'])
            if op == Token.TYPE.ADD:
                return lhs + rhs
            elif op == Token.TYPE.SUB:
                return lhs - rhs
            elif op == Token.TYPE.MOD:
                return lhs * rhs
            elif op == Token.TYPE.DIV:
                return lhs // rhs
            elif op == Token.TYPE.MOD:
                return lhs % rhs
        elif op == "DEBUG_PRINTU":
            result = _interpret_node(node[op])
            print(result)
            return None

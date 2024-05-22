#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Backend: Interpreter          ##
##-------------------------------##

## Imports
from ..frontend.node import Node, NodeBinExpr, NodeLiteral

## Constants
__all__: tuple[str] = ("interpret",)


## Constants
def interpret(ast: list[Node]) -> None:
    """"""
    for node in ast:
        if isinstance(node, NodeBinExpr):
            value = _interpret_binexpr(node)
            print(f"Value: {value}")


def _interpret_binexpr(node: Node) -> int:
    """"""
    if isinstance(node, NodeLiteral):
        return node.value
    assert(isinstance(node, NodeBinExpr))
    lhs = _interpret_binexpr(node.lhs)
    rhs = _interpret_binexpr(node.rhs)
    match node.type:
        case NodeBinExpr.Type.Add:
            return lhs + rhs
        case NodeBinExpr.Type.Sub:
            return lhs - rhs
        case NodeBinExpr.Type.Mul:
            return lhs * rhs
        case NodeBinExpr.Type.Div:
            return lhs // rhs
        case NodeBinExpr.Type.Mod:
            return lhs % rhs

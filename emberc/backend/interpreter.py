#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Backend: Interpreter          ##
##-------------------------------##

## Imports
from typing import Any
from ..frontend.node import Node, NodeAssignment, NodeBinExpr, NodeLiteral

## Constants
__all__: tuple[str] = ("interpret",)


## Constants
def interpret(ast: list[Node]) -> None:
    """"""
    variables: dict[str, Any] = {}
    for node in ast:
        if isinstance(node, NodeAssignment):
            name = node.name
            value = _interpret_binexpr(node.value, variables)
            variables[name] = value
        elif isinstance(node, NodeBinExpr):
            value = _interpret_binexpr(node, variables)
            print(f"Expr: {value}")
        elif isinstance(node, NodeLiteral):
            value = _interpret_literal(node, variables)
            print(f"Literal: {value}")

def _interpret_binexpr(node: Node, variables: dict[str, Any]) -> int:
    """"""
    if isinstance(node, NodeLiteral):
        return _interpret_literal(node, variables)
    assert(isinstance(node, NodeBinExpr))
    lhs = _interpret_binexpr(node.lhs, variables)
    rhs = _interpret_binexpr(node.rhs, variables)
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


def _interpret_literal(node: Node, variables: dict[str, Any]) -> int:
    """"""
    match node.type:
        case NodeLiteral.Type.Identifier:
            return variables[node.value]
        case NodeLiteral.Type.Integer:
            return node.value

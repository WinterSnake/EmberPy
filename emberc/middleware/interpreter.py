##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Visitor: Interpreter          ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import Any
from .nodes import (
    NodeStatementUnit,
    NodeExprBinary, NodeExprUnary, NodeExprLiteral,
)


## Classes
class InterpreterVisitor:
    """Simple AST Tree-Walking Interpreter"""

    # -Constructor
    def __init__(self, debug: bool = True) -> None:
        self.debug: bool = debug

    # -Instance Methods
    def visit_statement_unit(self, node: NodeStatementUnit) -> None:
        for node in node.nodes:
            value = node.accept(self)
            print(f"{node} = {value}")

    def visit_expression_binary(self, node: NodeExprBinary) -> int:
        if self.debug:
            print(f"{{ ExprBin::{node.type.name} | {node.location} }}")
        l_value = node.lhs.accept(self)
        r_value = node.rhs.accept(self)
        match node.type:
            case NodeExprBinary.Type.Add:
                return l_value + r_value
            case NodeExprBinary.Type.Sub:
                return l_value - r_value
            case NodeExprBinary.Type.Mul:
                return l_value * r_value
            case NodeExprBinary.Type.Div:
                return l_value // r_value
            case NodeExprBinary.Type.Mod:
                return l_value % r_value

    def visit_expression_unary(self, node: NodeExprUnary) -> int:
        if self.debug:
            print(f"{{ ExprUn::{node.type.name} | {node.location} }}")
        value = node.node.accept(self)
        match node.type:
            case NodeExprUnary.Type.Negative:
                return -value

    def visit_expression_group(self, node: NodeExprGroup) -> int:
        if self.debug:
            print(f"{{ ExprGrp::{node.location} }}")
        return node.inner_node.accept(self)

    def visit_expression_literal(self, node: NodeExprLiteral) -> int:
        if self.debug:
            print(f"{{ ExprLit::{node.value} | {node.location} }}")
        return node.value

    # -Static Methods
    @staticmethod
    def run(ast: Node, debug: bool = True) -> None:
        interpreter = InterpreterVisitor(debug)
        ast.accept(interpreter)

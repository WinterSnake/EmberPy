#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Pass: Optimization Folding    ##
##-------------------------------##

## Imports
from __future__ import annotations
from ..visitor import NodeVisitor
from ...frontend.node import Node, NodeAssignment, NodeBinExpr, NodeLiteral

## Constants
__all__: tuple[str] = ("FoldingOptimizationPass",)


## Classes
class FoldingOptimizationPass(NodeVisitor):
    """"""

    # -Instance Methods
    def visit_assignment(self, node: NodeAssignment) -> Node:
        ''''''
        node.value = node.value.visit(self)
        return node

    def visit_binexpr(self, node: NodeBinExpr) -> Node:
        ''''''
        lhs = node.lhs.visit(self)
        rhs = node.rhs.visit(self)
        if (
            lhs.type == NodeLiteral.Type.Identifier or
            rhs.type == NodeLiteral.Type.Identifier or
            isinstance(lhs, NodeBinExpr) or isinstance(rhs, NodeBinExpr)
        ):
            node.lhs = lhs
            node.rhs = rhs
            return node
        match node.type:
            case NodeBinExpr.Type.Add:
                value = lhs.value + rhs.value
            case NodeBinExpr.Type.Sub:
                value = lhs.value - rhs.value
            case NodeBinExpr.Type.Mul:
                value = lhs.value * rhs.value
            case NodeBinExpr.Type.Div:
                value = lhs.value // rhs.value
            case NodeBinExpr.Type.Mod:
                value = lhs.value % rhs.value
        return NodeLiteral(NodeLiteral.Type.Integer, value)

    def visit_literal(self, node: NodeLiteral) -> Node:
        ''''''
        return node

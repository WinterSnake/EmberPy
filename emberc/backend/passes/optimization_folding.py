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
from ...frontend.node import (
    Node, NodeDefinition, NodeAssignment, NodeBinExpr, NodeLiteral
)

## Constants
__all__: tuple[str] = ("FoldingOptimizationPass",)


## Classes
class FoldingOptimizationPass(NodeVisitor):
    """"""

    # -Instance Methods
    def visit_definition(self, node: NodeDefinition) -> Node:
        ''''''
        node.value = node.value.visit(self)
        return node

    def visit_assignment(self, node: NodeAssignment) -> Node:
        ''''''
        node.value = node.value.visit(self)
        return node

    def visit_binexpr(self, node: NodeBinExpr) -> Node:
        ''''''
        lhs = node.lhs.visit(self)
        rhs = node.rhs.visit(self)
        if (
            isinstance(lhs, NodeBinExpr) or isinstance(rhs, NodeBinExpr) or
            (isinstance(lhs, NodeLiteral) and lhs.type == NodeLiteral.Type.Identifier) or
            (isinstance(rhs, NodeLiteral) and rhs.type == NodeLiteral.Type.Identifier)
        ):
            node.lhs = lhs
            node.rhs = rhs
            return node
        assert(isinstance(lhs, NodeLiteral) and isinstance(lhs.value, int))
        assert(isinstance(rhs, NodeLiteral) and isinstance(rhs.value, int))
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

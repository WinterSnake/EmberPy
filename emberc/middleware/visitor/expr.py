##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Visitor: Expression           ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import TYPE_CHECKING, Protocol
from ..nodes import (
    NodeExprAssignment, NodeExprGroup,
    NodeExprBinary, NodeExprUnary,
    NodeExprVariable, NodeExprLiteral
)

if TYPE_CHECKING:
    from .visitor import NodeVisitor


## Classes
class NodeExprVisitor[TReturn](Protocol):
    """
    Node Visitor : Expression

    The node visitor for managing expression typed nodes
    """

    # -Instance Methods
    def visit_expr_assignment(self, node: NodeExprAssignment, manager: NodeVisitor) -> TReturn: ...
    def visit_expr_group(self, node: NodeExprGroup, manager: NodeVisitor) -> TReturn: ...
    def visit_expr_binary(self, node: NodeExprBinary, manager: NodeVisitor) -> TReturn: ...
    def visit_expr_unary(self, node: NodeExprUnary, manager: NodeVisitor) -> TReturn: ...
    def visit_expr_literal(self, node: NodeExprLiteral, manager: NodeVisitor) -> TReturn: ...
    def visit_expr_variable(self, node: NodeExprVariable, manager: NodeVisitor) -> TReturn: ...

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
    NodeExprGroup,
    NodeExprBinary, NodeExprUnary,
    NodeExprLiteral
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
    def visit_group(self, node: NodeExprGroup, manager: NodeVisitor) -> TReturn: ...
    def visit_binary(self, node: NodeExprBinary, manager: NodeVisitor) -> TReturn: ...
    def visit_unary(self, node: NodeExprUnary, manager: NodeVisitor) -> TReturn: ...
    def visit_literal(self, node: NodeExprLiteral, manager: NodeVisitor) -> TReturn: ...

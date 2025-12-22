##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Visitor: Statement            ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import TYPE_CHECKING, Protocol
from ..nodes import (
    NodeStmtBlock, NodeStmtConditional, NodeStmtExpression,
)

if TYPE_CHECKING:
    from .visitor import NodeVisitor


## Classes
class NodeStmtVisitor[TReturn](Protocol):
    """
    Node Visitor : Statement

    The node visitor for managing statement typed nodes
    """

    # -Instance Methods
    def visit_block(self, node: NodeStmtBlock, manager: NodeVisitor) -> TReturn: ...
    def visit_conditional(self, node: NodeStmtConditional, manager: NodeVisitor) -> TReturn: ...
    def visit_expression(self, node: NodeStmtExpression, manager: NodeVisitor) -> TReturn: ...

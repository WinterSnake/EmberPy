##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolved Node: Statement      ##
##-------------------------------##

## Imports
from typing import Protocol
from .node import (
    StmtNode,
    StmtEmptyNode,
)
from .expression import (
    StmtExpressionNode,
)

## Constants
__all__ = (
    "StmtNode",
    "StmtEmptyNode",
    "StmtExpressionNode",
)

## Classes
class StmtNodeVisitor[TReturn](Protocol):
    """A visitor pattern interface for traversing resolved statement nodes"""
    # -Instance Methods
    def visit_stmt_expression(self, node: StmtExpressionNode) -> TReturn: ...

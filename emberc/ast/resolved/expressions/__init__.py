##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolved Node: Expression     ##
##-------------------------------##

## Imports
from typing import Protocol
from .binary import (
    ExprAssignNode,
    ExprBinaryNode,
)
from .literal import (
    ExprIntegerNode,
    ExprVariableNode,
)
from .node import ExprNode

## Constants
__all__ = (
    "ExprNode",
    "ExprAssignNode",
    "ExprBinaryNode",
    "ExprIntegerNode",
    "ExprVariableNode",
)

## Classes
class ExprNodeVisitor[TReturn](Protocol):
    """A visitor pattern interface for traversing resolved expression nodes."""
    # -Instance Methods
    def visit_expr_assignment(self, node: ExprAssignNode) -> TReturn: ...
    def visit_expr_binary(self, node: ExprBinaryNode) -> TReturn: ...
    def visit_expr_integer(self, node: ExprIntegerNode) -> TReturn: ...
    def visit_expr_variable(self, node: ExprVariableNode) -> TReturn: ...

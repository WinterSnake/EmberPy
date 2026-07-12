##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolved Node: Declaration    ##
##-------------------------------##

## Imports
from typing import Protocol
from .node import (
    DeclNode,
    DeclUnitNode,
    DeclSequenceNode,
)
from .variable import DeclVariableNode

## Constants
__all__ = (
    "DeclNode",
    "DeclUnitNode",
    "DeclSequenceNode",
    "DeclVariableNode",
)

## Classes
class DeclNodeVisitor[TReturn](Protocol):
    """A visitor pattern interface for traversing resolved declaration nodes."""
    # -Instance Methods
    def visit_unit(self, node: DeclUnitNode) -> TReturn: ...
    def visit_variable(self, node: DeclVariableNode) -> TReturn: ...

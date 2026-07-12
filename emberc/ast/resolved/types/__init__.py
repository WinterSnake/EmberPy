##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolved Node: Type           ##
##-------------------------------##

## Imports
from typing import Protocol
from .node import (TypeNode, TypePending)
from .primitive import TypePrimitive

## Constants
__all__ = (
    "TypeNode",
    "TypePending",
    "TypePrimitive",
)

## Classes
class TypeNodeVisitor[TReturn](Protocol):
    """A visitor pattern interface for traversing resolved type nodes."""
    # -Instance Methods
    def visit_type_primitive(self, node: TypePrimitive) -> TReturn: ...

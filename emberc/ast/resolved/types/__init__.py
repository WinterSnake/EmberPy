##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolved Node: Type           ##
##-------------------------------##

## Imports
from typing import Protocol
from .node import TypeNode
from .primitive import TypePrimitive

## Constants
__all__ = (
    "TypeNode",
    "TypePrimitive",
)

## Classes
class TypeNodeVisitor[TReturn](Protocol):
    """
    A structural protocol implementing the visitor pattern for resolved semantic type nodes.
    """
    # -Instance Methods
    def visit_primitive(self, node: TypePrimitive) -> TReturn: ...

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## AST: Resolved                 ##
##-------------------------------##

## Imports
from .types import (
    TypeNode,
    TypePrimitive,
)

## Constants
__all__ = (
    "ResolvedNode",
    # -Types
    "TypeNode",
    "TypePrimitive",
)
type ResolvedNode = TypeNode

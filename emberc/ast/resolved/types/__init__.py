##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolved Node: Type           ##
##-------------------------------##

## Imports
from .array import NodeTypePendingArray, NodeTypeArray
from .base import NodeType
from .function import NodeTypeFunction
from .identifier import NodeTypeIdentifier
from .pointer import NodeTypePointer
from .primitive import NodeTypePrimitive
from .slice import NodeTypeSlice
from .visitor import NodeTypeVisitor, NodeTypePendingVisitor

## Constants
__all__ = (
    # -Core
    "NodeType",
    "NodeTypePrimitive", "NodeTypeArray", "NodeTypeIdentifier",
    "NodeTypePointer", "NodeTypeSlice", "NodeTypeFunction",
    # -Pending
    "NodeTypePendingArray",
    # -Visitors
    "NodeTypeVisitor", "NodeTypePendingVisitor",
)

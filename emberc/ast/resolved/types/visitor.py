##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolved Node: Type Visitor   ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .array import NodeTypePendingArray, NodeTypeArray
    from .base import NodeType
    from .function import NodeTypeFunction
    from .identifier import NodeTypeIdentifier
    from .pointer import NodeTypePointer
    from .primitive import NodeTypePrimitive
    from .slice import NodeTypeSlice


## Classes
class NodeTypeVisitor[TReturn](Protocol):
    """
    """
    # -Instance Methods
    def visit_type_primitive(self, node: NodeTypePrimitive) -> TReturn: ...
    def visit_type_array(self, node: NodeTypeArray) -> TReturn: ...
    def visit_type_identifier(self, node: NodeTypeIdentifier) -> TReturn: ...
    def visit_type_function(self, node: NodeTypeFunction) -> TReturn: ...
    def visit_type_pointer(self, node: NodeTypePointer) -> TReturn: ...
    def visit_type_slice(self, node: NodeTypeSlice) -> TReturn: ...


class NodeTypePendingVisitor[TReturn](NodeTypeVisitor[TReturn], Protocol):
    """
    """
    # -Instance Methods
    def visit_type_array_pending(self, node: NodeTypePendingArray) -> TReturn: ...

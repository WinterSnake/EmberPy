##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type Node: Pointer            ##
##-------------------------------##

## Imports
from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .base import NodeType

if TYPE_CHECKING:
    from .visitor import NodeTypeVisitor
    from ...unresolved import UnresolvedNodeVisitor


## Classes
@dataclass(frozen=True, slots=True)
class NodeTypePointer(NodeType):
    """
    Ember Type: Pointer

    A type representing a pointer to a target type
    """
    # -Instance Methods
    def accept[T](self, visitor: NodeTypeVisitor[T]) -> T:
        return visitor.visit_type_pointer(self)

    def bind[T](self, visitor: UnresolvedNodeVisitor[T]) -> None:
        self.target.bind(visitor)

    # -Properties
    target: NodeType

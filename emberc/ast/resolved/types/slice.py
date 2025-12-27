##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type Node: Slices             ##
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
@dataclass(slots=True)
class NodeTypeSlice(NodeType):
    """
    Ember Type: Slice

    A type representing a slice to a target type
    """
    # -Instance Methods
    def accept[T](self, visitor: NodeTypeVisitor[T]) -> T:
        return visitor.visit_type_slice(self)

    def bind[T](self, visitor: UnresolvedNodeVisitor[T]) -> None:
        self.target.bind(visitor)

    # -Properties
    many_to_one: bool
    target: NodeType

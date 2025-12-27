##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type Node: Array              ##
##-------------------------------##

## Imports
from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, cast
from .base import NodeType
from .visitor import NodeTypePendingVisitor

if TYPE_CHECKING:
    from collections.abc import Sequence
    from .visitor import NodeTypeVisitor
    from ...unresolved import UnresolvedNode, UnresolvedNodeVisitor


## Classes
@dataclass
class NodeTypePendingArray(NodeType):
    """
    Ember Pending Type: Array

    A type representing an array that has not been bound
    to it's respective dimensions. Needs to be analyzed further
    to gain full context and be built into an ArrayType node
    """
    # -Instance Methods
    def accept[T](self, visitor: NodeTypeVisitor[T]) -> T:
        ext_visitor = cast(NodeTypePendingVisitor[T], visitor)
        return ext_visitor.visit_type_array_pending(self)

    def bind[T](self, visitor: UnresolvedNodeVisitor[T]) -> None:
        self.target.bind(visitor)
        for dimension in self.dimensions:
            visitor.visit(dimension)

    # -Properties
    target: NodeType
    dimensions: Sequence[UnresolvedNode]


@dataclass(slots=True)
class NodeTypeArray(NodeType):
    """
    Ember Type: Array

    A type representing an array and it's dimensions
    """
    # -Instance Methods
    def accept[T](self, visitor: NodeTypeVisitor[T]) -> T:
        return visitor.visit_type_array(self)

    def bind[T](self, visitor: UnresolvedNodeVisitor[T]) -> None: ...

    # -Properties
    target: NodeType
    dimensions: tuple[int, ...]
    is_jagged: bool = False

    @property
    def dimension_count(self) -> int:
        return len(self.dimensions)

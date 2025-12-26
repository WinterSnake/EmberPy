##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type Node: Function           ##
##-------------------------------##

## Imports
from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .base import NodeType

if TYPE_CHECKING:
    from collections.abc import Collection
    from .visitor import NodeTypeVisitor
    from ...unresolved import UnresolvedNodeVisitor


## Classes
@dataclass(frozen=True, slots=True)
class NodeTypeFunction(NodeType):
    """
    Ember Type: Function

    A type representing the function signature (return + parameters)
    """
    # -Instance Methods
    def accept[T](self, visitor: NodeTypeVisitor[T]) -> T:
        return visitor.visit_type_function(self)

    def bind[T](self, visitor: UnresolvedNodeVisitor[T]) -> None:
        self.return_type.bind(visitor)
        for parameter_type in self.parameter_types:
            parameter_type.bind(visitor)

    # -Properties
    return_type: NodeType
    parameter_types: Collection[NodeType]

    @property
    def arity(self) -> int:
        return len(self.parameter_types)

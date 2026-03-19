##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Literal      ##
##-------------------------------##

## Imports
from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from ...core import MutableCollection

## Constants
type AST_LITERAL_TYPES = bool | int | str


## Classes
@dataclass
class UnresolvedArrayNode(UnresolvedNode):
    """
    Unresolved AST Node: Array

    A leaf container for holding a collection of values.
    """
    # -Dunder Methods
    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, i: int) -> UnresolvedNode:
        return self.values[i]

    def __setitem__(self, i: int, value:  UnresolvedNode) -> None:
        self.values[i] = value

    # -Properties
    values: MutableCollection[UnresolvedNode]


@dataclass
class UnresolvedLiteralNode(UnresolvedNode):
    """
    Unresolved AST Node: Literal

    A leaf container for holding a primitive constant value.
    """
    # -Instance Methods
    def value_as[T: AST_LITERAL_TYPES](self, _type: type[T]) -> T:
        assert type(self.value) is _type, "TODO: Error handling"
        return self.value

    # -Properties
    kind: UnresolvedLiteralNode.Kind
    value: AST_LITERAL_TYPES

    # -Sub-Classes
    class Kind(IntEnum):
        Boolean = auto()
        Integer = auto()

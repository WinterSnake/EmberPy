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
from .node import UnresolvedNode

## Constants
type AST_LITERAL_TYPES = bool | int | str


## Classes
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

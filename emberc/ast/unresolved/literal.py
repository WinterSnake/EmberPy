##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Literal      ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Collection
from dataclasses import dataclass
from enum import IntEnum, auto
from .node import UnresolvedNode

## Constants
type LITERAL_VALUE = bool | int | str


## Classes
@dataclass
class UnresolvedLiteralNode(UnresolvedNode):
    """
    Ember Unresolved Node: Literal

    A node for storing a literal value
    """
    # -Properties
    value: LITERAL_VALUE
    type: UnresolvedLiteralNode.Type
    # -Sub-Classes
    class Type(IntEnum):
        Integer = auto()
        Boolean = auto()


@dataclass
class UnresolvedArrayNode(UnresolvedNode):
    """
    Ember Unresolved Node: Array

    A node for storing a array values
    """
    # -Properties
    values: Collection[UnresolvedNode]

    @property
    def count(self) -> int:
        return len(self.values)


@dataclass
class UnresolvedExprEmptyNode(UnresolvedNode):
    """
    Ember Unresolved Node: Empty Expression

    A placeholder node for storing an empty expression
    Used for range and index postfix context
    """
    pass

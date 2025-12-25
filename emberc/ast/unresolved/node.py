##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node               ##
##-------------------------------##

## Imports
from __future__ import annotations
from abc import ABC
from collections.abc import Collection
from enum import IntEnum, auto
from dataclasses import dataclass
from ...location import Location


## Classes
@dataclass
class UnresolvedNode(ABC):
    """
    Ember AST Node: Unresolved

    An unresolved abstract node
    """
    # -Properties
    location: Location


@dataclass
class UnresolvedUnitNode(UnresolvedNode):
    """
    Ember Unresolved Node: Unit

    An AST unit container for parser output
    """
    # -Constructor
    def __init__(self, children: Collection[UnresolvedNode]) -> None:
        super().__init__(None)  # type: ignore
        self.children = children

    # -Properties
    children: Collection[UnresolvedNode]


@dataclass
class UnresolvedTypeNode(UnresolvedNode):
    """
    Ember Unresolved Node: Type

    A node for storing a builtin type set
    """
    # -Properties
    type: UnresolvedTypeNode.Type
    # -Sub-Classes
    class Type(IntEnum):
        Void = auto()
        Boolean = auto()
        Int8 = auto()
        Int16 = auto()
        Int32 = auto()
        Int64 = auto()
        UInt8 = auto()
        UInt16 = auto()
        UInt32 = auto()
        UInt64 = auto()

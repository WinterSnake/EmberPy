##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Type         ##
##-------------------------------##

## Imports
from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum, auto
from .node import UnresolvedNode


## Classes
@dataclass
class UnresolvedTypeNode(UnresolvedNode):
    """
    Unresolved AST Node: Type

    A representation for primitive types.
    """
    # -Properties
    kind: UnresolvedTypeNode.Kind

    # -Sub-Classes
    class Kind(IntEnum):
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
        SSize = auto()
        USize = auto()


@dataclass
class UnresolvedModifierNode(UnresolvedNode):
    """
    Unresolved AST Node: Type Modifier

    A representation for a unary type modifiers.
    """
    # -Properties
    kind: UnresolvedModifierNode.Kind
    target: UnresolvedNode

    # -Sub-Classes
    class Kind(IntEnum):
        Const = auto()

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Unary        ##
##-------------------------------##

## Imports
from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from collections.abc import Sequence


## Classes
@dataclass
class UnresolvedUnaryPrefixNode(UnresolvedNode):
    """
    Ember Unresolved Node: Unary Prefix

    A node for storing a unary prefix operator and operand
    """
    # -Properties
    operator: UnresolvedUnaryPrefixNode.Operator
    operand: UnresolvedNode
    # -Sub-Classes
    class Operator(IntEnum):
        # -Math
        Negative = auto()
        LogNeg = auto()
        BitNeg = auto()
        # -Pointers
        Ptr = auto()
        Ref = auto()
        Deref = auto()
        Slice = auto()
        SlicePtr = auto()


@dataclass
class UnresolvedUnaryModifierNode(UnresolvedNode):
    """
    Ember Unresolved Node: Unary Modifier

    A node for storing a unary type modifier and it's target node
    """
    # -Properties
    type: UnresolvedUnaryModifierNode.Type
    target: UnresolvedNode
    # -Sub-Classes
    class Type(IntEnum):
        Static = auto()
        Const = auto()
        Immut = auto()


@dataclass
class UnresolvedUnaryPostfixNode(UnresolvedNode):
    """
    Ember Unresolved Node: Unary Postfix

    A node for storing a unary postfix head and kind
    """
    # -Properties
    head: UnresolvedNode
    kind: UnresolvedUnaryPostfixNode.Kind
    arguments: Sequence[UnresolvedNode]

    @property
    def argument_count(self) -> int:
        return len(self.arguments)

    # -Sub-Classes
    class Kind(IntEnum):
        Call = auto()
        Subscript = auto()

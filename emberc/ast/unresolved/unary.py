##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Unary        ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Collection
from dataclasses import dataclass
from enum import IntEnum, auto
from .node import UnresolvedNode


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
class UnresolvedUnaryPostfixNode(UnresolvedNode):
    """
    Ember Unresolved Node: Unary Postfix

    A node for storing a unary postfix head and kind
    """
    # -Properties
    head: UnresolvedNode
    kind: UnresolvedUnaryPostfixNode.Kind
    arguments: Collection[UnresolvedNode]
    # -Sub-Classes
    class Kind(IntEnum):
        Call = auto()
        Subscript = auto()

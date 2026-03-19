##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Unary        ##
##-------------------------------##

## Imports
from __future__ import annotations
from dataclasses import dataclass, field
from enum import IntEnum, auto
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from ...core import MutableCollection


## Classes
@dataclass
class UnresolvedUnaryPrefixNode(UnresolvedNode):
    """
    Unresolved AST Node: Unary Prefix

    A container for holding a unary prefix operator and its operand.
    """
    # -Properties
    operator: UnresolvedUnaryPrefixNode.Operator
    operand: UnresolvedNode

    # -Sub-Classes
    class Operator(IntEnum):
        # -Math
        NumericalNegate = auto()
        LogicalNegate = auto()
        BitwiseNegate = auto()
        # -Memory
        Pointer = auto()
        AddressOf = auto()
        Dereference = auto()


@dataclass
class UnresolvedUnaryPostfixNode(UnresolvedNode):
    """
    Unresolved AST Node: Unary Postfix

    A container for holding a unary postfix operator and its operand.
    """
    # -Properties
    head: UnresolvedNode
    kind: UnresolvedUnaryPostfixNode.Kind
    arguments: MutableCollection[UnresolvedNode]

    @property
    def argument_count(self) -> int:
        return len(self.arguments)

    # -Sub-Classes
    class Kind(IntEnum):
        Call = auto()

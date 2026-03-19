##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Binary       ##
##-------------------------------##

## Imports
from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum, auto
from .node import UnresolvedNode


## Classes
@dataclass
class UnresolvedBinaryNode(UnresolvedNode):
    """
    Unresolved AST Node: Binary

    A container for holding a left and right hand operand
    and the appropriate operator between the two expressions.
    """
    # -Properties
    operator: UnresolvedBinaryNode.Operator
    lhs: UnresolvedNode
    rhs: UnresolvedNode

    # -Sub-Classes
    class Operator(IntEnum):
        Range = auto()
        # -Math
        Add = auto()
        Sub = auto()
        Mul = auto()
        Div = auto()
        Mod = auto()
        # -Bitwise
        BitXor = auto()
        BitAnd = auto()
        BitOr = auto()
        ShiftL = auto()
        ShiftR = auto()
        # -Comparisons
        LogOr = auto()
        LogAnd = auto()
        Eq = auto()
        NtEq = auto()
        Lt = auto()
        Gt = auto()
        LtEq = auto()
        GtEq = auto()

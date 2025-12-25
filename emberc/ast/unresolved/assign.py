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
class UnresolvedAssignNode(UnresolvedNode):
    """
    Ember Unresolved Node: Assignment

    A node for storing an assignment with l_value, operator, and r_value
    """
    # -Properties
    operator: UnresolvedAssignNode.Operator
    l_value: UnresolvedNode
    r_value: UnresolvedNode
    # -Sub-Classes
    class Operator(IntEnum):
        Eq = auto()
        AddEq = auto()
        SubEq = auto()
        MulEq = auto()
        DivEq = auto()
        ModEq = auto()
        BitNegEq = auto()
        BitXorEq = auto()
        BitAndEq = auto()
        BitOrEq = auto()
        ShiftLEq = auto()
        ShiftREq = auto()

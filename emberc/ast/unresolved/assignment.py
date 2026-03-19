##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Assignment   ##
##-------------------------------##

## Imports
from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum, auto
from .node import UnresolvedNode


## Classes
@dataclass
class UnresolvedAssignmentNode(UnresolvedNode):
    """
    Unresolved AST Node: Assign

    A container for holding a left and right value operand
    and the appropriate assignment operator between the two values.
    """
    # -Properties
    operator: UnresolvedAssignmentNode.Operator
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
        BitXorEq = auto()
        BitAndEq = auto()
        BitOrEq = auto()
        ShiftLEq = auto()
        ShiftREq = auto()

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Expression Binary       ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from .expr import NodeExpr
from ...location import Location


## Classes
class NodeExprBinary(NodeExpr):
    """
    Ember Expression Node : Binary
    Represents an AST node of a binary expression with it's operator
    """

    # -Constructor
    def __init__(
        self, location: Location, operator: NodeExprBinary.Operator,
        lhs: NodeExpr, rhs: NodeExpr
    ) -> None:
        super().__init__(location)
        self.operator: NodeExprBinary.Operator = operator
        self.lhs: NodeExpr = lhs
        self.rhs: NodeExpr = rhs

    # -Dunder Methods
    def __str__(self) -> str:
        return f"({self.lhs}{OPERATOR_STR[self.operator]}{self.rhs})"

    # -Sub-Classes
    class Operator(IntEnum):
        # -Math
        Add = auto()
        Sub = auto()
        Mul = auto()
        Div = auto()
        Mod = auto()


## Body
OPERATOR_STR = {
    NodeExprBinary.Operator.Add: '+',
    NodeExprBinary.Operator.Sub: '-',
    NodeExprBinary.Operator.Mul: '*',
    NodeExprBinary.Operator.Div: '/',
    NodeExprBinary.Operator.Mod: '%',
}

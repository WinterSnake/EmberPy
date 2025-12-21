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
class NodeExprUnary(NodeExpr):
    """
    Ember Expression Node : Unary
    Represents an AST node of a unary expression with it's operator
    """

    # -Constructor
    def __init__(
        self, location: Location, operator: NodeExprUnary.Operator,
        expression: NodeExpr
    ) -> None:
        super().__init__(location)
        self.operator: NodeExprUnary.Operator = operator
        self.expression: NodeExpr = expression

    # -Dunder Methods
    def __str__(self) -> str:
        return f"({OPERATOR_STR[self.operator]}{self.expression})"

    # -Sub-Classes
    class Operator(IntEnum):
        # -Math
        Negative = auto()


## Body
OPERATOR_STR = {
    NodeExprUnary.Operator.Negative: '-',
}

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: ExprBinary              ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import Any
from .core import NodeExpr
from .visitor import NodeVisitor
from ...location import Location


## Classes
class NodeExprBinary(NodeExpr):
    """
    Ember Node: Expression :: Binary
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

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_binary(self)

    # -Sub-Classes
    class Operator(IntEnum):
        # -Math
        Add = auto()
        Sub = auto()
        Mul = auto()
        Div = auto()
        Mod = auto()
        # -Comparisons
        Lt = auto()
        Gt = auto()
        LtEq = auto()
        GtEq = auto()
        EqEq = auto()
        NtEq = auto()

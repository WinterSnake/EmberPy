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


## Functions
def _operator_to_str(operator: NodeExprBinary.Operator) -> str:
    """Returns the operator as a string representation"""
    match operator:
        case NodeExprBinary.Operator.Add:
            return '+'
        case NodeExprBinary.Operator.Sub:
            return '-'
        case NodeExprBinary.Operator.Mul:
            return '*'
        case NodeExprBinary.Operator.Div:
            return '/'
        case NodeExprBinary.Operator.Mod:
            return '%'


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

    # -Dunder Methods
    def __str__(self) -> str:
        return f"({self.lhs} {self.rhs} {_operator_to_str(self.operator)})"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_binary(self)

    # -Sub-Classes
    class Operator(IntEnum):
        Add = auto()
        Sub = auto()
        Mul = auto()
        Div = auto()
        Mod = auto()

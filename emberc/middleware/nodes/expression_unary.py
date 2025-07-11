##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Expression - Unary      ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import Any
from .core import NodeExpr
from .visitor import NodeVisitor
from ...location import Location


## Functions
def _get_operator_str(_type: NodeExprUnary.Type) -> str:
    """Returns the char/string of a given unary operator"""
    match _type:
        case NodeExprUnary.Type.Negate:
            return '!'
        case NodeExprUnary.Type.Negative:
            return '-'


## Classes
class NodeExprUnary(NodeExpr):
    """
    Ember Node: Expression :: Unary
    Represents an AST node of a unary expression with its operator
    """

    # -Constructor
    def __init__(
        self, location: Location, operator: NodeExprUnary.Type, expression: NodeExpr
    ) -> None:
        super().__init__(location)
        self.operator: NodeExprUnary.Type = operator
        self.expression: NodeExpr = expression

    # -Dunder Methods
    def __str__(self) -> str:
        return f"({self.expression} {_get_operator_str(self.operator)})"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_unary(self)

    # -Sub-Classes
    class Type(IntEnum):
        '''Unary Operator Type'''
        Negate = auto()
        Negative = auto()

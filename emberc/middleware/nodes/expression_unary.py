##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node::Expression - Unary      ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import Any
from .core import NodeExpr
from .visitor import NodeVisitor
from ...location import Location


## Functions
def _unary_type_to_str(_type: NodeExprUnary.Type) -> str:
    """Returns a char of the operator passed in"""
    match _type:
        case NodeExprUnary.Type.Negative:
            return '-'


## Classes
class NodeExprUnary(NodeExpr):
    """
    Ember Expression Node: Unary
    Represents a unary expression node with operator and leaf node
    """

    # -Constructor
    def __init__(
        self, location: Location, _type: NodeExprUnary.Type, value: NodeExpr
    ) -> None:
        super().__init__(location)
        self.type: NodeExprUnary.Type = _type
        self.value: NodeExpr = value

    # -Dunder Methods
    def __str__(self) -> str:
        return f"({self.value} {_unary_type_to_str(self.type)})"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_unary(self)

    # -Sub-Classes
    class Type(IntEnum):
        '''Unary Operator Type'''
        Negative = auto()

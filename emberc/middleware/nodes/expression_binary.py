##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node::Expression - Binary     ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import Any
from .core import NodeExpr
from .visitor import NodeVisitor
from ...location import Location


## Functions
def _binary_type_to_str(_type: NodeExprBinary.Type) -> str:
    """Returns a char of the operator passed in"""
    match _type:
        case NodeExprBinary.Type.Add:
            return '+'
        case NodeExprBinary.Type.Sub:
            return '-'
        case NodeExprBinary.Type.Mul:
            return '*'
        case NodeExprBinary.Type.Div:
            return '/'
        case NodeExprBinary.Type.Mod:
            return '%'
        case NodeExprBinary.Type.Lt:
            return '<'
        case NodeExprBinary.Type.Gt:
            return '>'
        case NodeExprBinary.Type.LtEq:
            return '<='
        case NodeExprBinary.Type.GtEq:
            return '>='
        case NodeExprBinary.Type.EqEq:
            return '=='
        case NodeExprBinary.Type.NtEq:
            return '!='


## Classes
class NodeExprBinary(NodeExpr):
    """
    Ember Expression Node: Binary
    Represents a binary expression node with lhs, rhs and the operator
    """

    # -Constructor
    def __init__(
        self, location: Location, _type: NodeExprBinary.Type,
        lhs: NodeExpr, rhs: NodeExpr
    ) -> None:
        super().__init__(location)
        self.type: NodeExprBinary.Type = _type
        self.lhs: NodeExpr = lhs
        self.rhs: NodeExpr = rhs

    # -Dunder Methods
    def __str__(self) -> str:
        return f"({self.lhs} {self.rhs} {_binary_type_to_str(self.type)})"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_binary(self)

    # -Sub-Classes
    class Type(IntEnum):
        '''Binary Operator Type'''
        Add = auto()
        Sub = auto()
        Mul = auto()
        Div = auto()
        Mod = auto()
        Lt = auto()
        Gt = auto()
        LtEq = auto()
        GtEq = auto()
        EqEq = auto()
        NtEq = auto()

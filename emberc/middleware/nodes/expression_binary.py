##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Expression - Binary     ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import Any
from .core import NodeExpr
from .visitor import NodeVisitor
from ...location import Location


## Functions
def _get_operator_str(_type: NodeExprBinary.Type) -> str:
    """Returns the char/string of a given binary operator"""
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
            return "<="
        case NodeExprBinary.Type.GtEq:
            return ">="
        case NodeExprBinary.Type.EqEq:
            return "=="
        case NodeExprBinary.Type.NtEq:
            return "!="


## Classes
class NodeExprBinary(NodeExpr):
    """
    Ember Node: Expression :: Binary
    Represents an AST node of a binary expression with its operator
    """

    # -Constructor
    def __init__(
            self, location: Location, operator: NodeExprBinary.Type,
            lhs: NodeExpr, rhs: NodeExpr
    ) -> None:
        super().__init__(location)
        self.operator: NodeExprBinary.Type = operator
        self.lhs: NodeExpr = lhs
        self.rhs: NodeExpr = rhs

    # -Dunder Methods
    def __str__(self) -> str:
        return f"({self.lhs} {self.rhs} {_get_operator_str(self.operator)})"

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

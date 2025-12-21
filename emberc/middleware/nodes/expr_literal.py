##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Expression Literal      ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from .expr import NodeExpr
from ...location import Location

## Constants
type LITERAL = int


## Classes
class NodeExprLiteral(NodeExpr):
    """
    Ember Expression Node : Literal
    Represents an AST node of a constant literal with it's value
    """

    # -Constructor
    def __init__(
        self, location: Location, _type: NodeExprLiteral.Type, value: LITERAL
    ) -> None:
        super().__init__(location)
        self.type: NodeExprLiteral.Type = _type
        self.value: LITERAL = value

    # -Dunder Methods
    def __str__(self) -> str:
        return str(self.value)

    # -Static Methods
    @staticmethod
    def create_integer(location: Location, value: int) -> NodeExprLiteral:
        return NodeExprLiteral(location, NodeExprLiteral.Type.Integer, value)

    # -Sub-Classes
    class Type(IntEnum):
        Integer = auto()

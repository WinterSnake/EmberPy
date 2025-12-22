##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Expression Literal      ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import TYPE_CHECKING
from .expr import NodeExpr
from ...location import Location

if TYPE_CHECKING:
    from ..visitor import NodeVisitor, NodeExprVisitor

## Constants
type VALUE_TYPES = bool | int


## Classes
class NodeExprLiteral(NodeExpr):
    """
    Ember Expression Node : Literal
    Represents an AST node of a constant literal with it's value
    """

    # -Constructor
    def __init__(
        self, location: Location, _type: NodeExprLiteral.Type, value: VALUE_TYPES
    ) -> None:
        super().__init__(location)
        self.type: NodeExprLiteral.Type = _type
        self.value: VALUE_TYPES = value

    # -Instance Methods
    def accept[T](self, visitor: NodeExprVisitor[T], manager: NodeVisitor) -> T:
        return visitor.visit_expr_literal(self, manager)

    # -Static Methods
    @staticmethod
    def create_boolean(location: Location, value: bool) -> NodeExprLiteral:
        return NodeExprLiteral(location, NodeExprLiteral.Type.Boolean, value)

    @staticmethod
    def create_integer(location: Location, value: int) -> NodeExprLiteral:
        return NodeExprLiteral(location, NodeExprLiteral.Type.Integer, value)

    # -Sub-Classes
    class Type(IntEnum):
        Integer = auto()
        Boolean = auto()

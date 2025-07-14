##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: ExprLiteral             ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import Any
from .core import NodeExpr
from .visitor import NodeVisitor
from ...location import Location

## Constants
LITERAL = int


## Classes
class NodeExprLiteral(NodeExpr):
    """
    Ember Node: Expression :: Literal
    Represents an AST node of a constant literal with it's value
    """

    # -Constructor
    def __init__(
        self, location: Location, _type: NodeExprLiteral.Type, value: LITERAL
    ) -> None:
        super().__init__(location)
        self.type: NodeExprLiteral.Type = _type
        self.value: LITERAL = value

    # -Dunder Method
    def __str__(self) -> str:
        match self.type:
            case NodeExprLiteral.Type.Integer:
                return str(self.value)

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_literal(self)

    # -Sub-Classes
    class Type(IntEnum):
        Integer = auto()

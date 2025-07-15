##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: ExprUnary               ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import Any
from .core import NodeExpr
from .visitor import NodeVisitor
from ...location import Location


## Classes
class NodeExprUnary(NodeExpr):
    """
    Ember Node: Expression :: Unary
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

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_unary(self)

    # -Sub-Classes
    class Operator(IntEnum):
        Minus = auto()

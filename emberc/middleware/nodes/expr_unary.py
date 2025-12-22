##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Expression Binary       ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import TYPE_CHECKING
from .expr import NodeExpr
from ...location import Location

if TYPE_CHECKING:
    from ..visitor import NodeVisitor, NodeExprVisitor


## Classes
class NodeExprUnary(NodeExpr):
    """
    Ember Expression Node : Unary
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
    def accept[T](self, visitor: NodeExprVisitor[T], manager: NodeVisitor) -> T:
        return visitor.visit_expr_unary(self, manager)

    # -Sub-Classes
    class Operator(IntEnum):
        # -Math
        Negate = auto()
        Negative = auto()

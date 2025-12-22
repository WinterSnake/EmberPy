##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Expression Assignment   ##
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
type LITERAL_VALUE = bool | int


## Classes
class NodeExprAssignment(NodeExpr):
    """
    Ember Expression Node : Assignment
    Represents an AST node of an assignment expression with it's l-value and r-value
    """

    # -Constructor
    def __init__(
        self, location: Location, l_value: NodeExpr, r_value: NodeExpr
    ) -> None:
        super().__init__(location)
        self.l_value: NodeExpr = l_value
        self.r_value: NodeExpr = r_value

    # -Dunder Methods
    def __str__(self) -> str:
        return f"[{self.l_value} = {self.r_value}]"

    # -Instance Methods
    def accept[T](self, visitor: NodeExprVisitor[T], manager: NodeVisitor) -> T:
        return visitor.visit_assignment(self, manager)

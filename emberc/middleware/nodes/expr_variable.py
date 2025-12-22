##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Expression Variable     ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import TYPE_CHECKING
from .expr import NodeExpr
from ...location import Location

if TYPE_CHECKING:
    from ..visitor import NodeVisitor, NodeExprVisitor


## Classes
class NodeExprVariable(NodeExpr):
    """
    Ember Expression Node : Variable
    Represents an AST node of a variable expression
    """

    # -Constructor
    def __init__(self, location: Location, _id: str) -> None:
        super().__init__(location)
        self.id: str = _id

    # -Dunder Methods
    def __str__(self) -> str:
        return f"Variable({self.id})"

    # -Instance Methods
    def accept[T](self, visitor: NodeExprVisitor[T], manager: NodeVisitor) -> T:
        return visitor.visit_variable(self, manager)

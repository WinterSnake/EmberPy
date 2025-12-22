##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Statement Expression    ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import TYPE_CHECKING
from .expr import NodeExpr
from .stmt import NodeStmt
from ...location import Location

if TYPE_CHECKING:
    from ..visitor import NodeVisitor, NodeStmtVisitor


## Classes
class NodeStmtLoop(NodeStmt):
    """
    Ember Statement Node : Loop
    Represents an AST node of a conditional loop
    """

    # -Constructor
    def __init__(
        self, location: Location, condition: NodeExpr, body: NodeStmt
    ) -> None:
        super().__init__(location)
        self.condition: NodeExpr = condition
        self.body: NodeStmt = body

    # -Instance Methods
    def accept[T](self, visitor: NodeStmtVisitor[T], manager: NodeVisitor) -> T:
        return visitor.visit_stmt_loop(self, manager)

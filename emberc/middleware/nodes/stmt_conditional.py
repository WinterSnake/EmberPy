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
class NodeStmtConditional(NodeStmt):
    """
    Ember Statement Node : Conditional
    Represents an AST node of a conditional statement
    """

    # -Constructor
    def __init__(
        self, location: Location, condition: NodeExpr,
        body: NodeStmt, else_body: NodeStmt | None
    ) -> None:
        super().__init__(location)
        self.condition: NodeExpr = condition
        self.body: NodeStmt = body
        self.else_body: NodeStmt | None = else_body

    # -Instance Methods
    def accept[T](self, visitor: NodeStmtVisitor[T], manager: NodeVisitor) -> T:
        return visitor.visit_stmt_conditional(self, manager)

    # -Properties
    @property
    def has_else_body(self) -> bool:
        return self.else_body is not None

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
class NodeStmtReturn(NodeStmt):
    """
    Ember Statement Node : Return
    Represents an AST node of a returned expression
    """

    # -Constructor
    def __init__(self, location: Location, value: NodeExpr | None) -> None:
        super().__init__(location)
        self._value: NodeExpr | None = value

    # -Instance Methods
    def accept[T](self, visitor: NodeStmtVisitor[T], manager: NodeVisitor) -> T:
        return visitor.visit_stmt_return(self, manager)

    # -Properties
    @property
    def has_value(self) -> bool:
        return self._value is not None

    @property
    def value(self) -> NodeExpr:
        assert self._value is not None
        return self._value

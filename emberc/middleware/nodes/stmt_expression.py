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
class NodeStmtExpression(NodeStmt):
    """
    Ember Statement Node : Expression
    Represents an AST node of a statement with an expression
    """

    # -Constructor
    def __init__(self, location: Location, expression: NodeExpr | None) -> None:
        super().__init__(location)
        self._expression: NodeExpr | None = expression

    # -Dunder Methods
    def __str__(self) -> str:
        if self.is_empty:
            return ";"
        return f"{self.expression};"

    # -Instance Methods
    def accept[T](self, visitor: NodeStmtVisitor[T], manager: NodeVisitor) -> T:
        return visitor.visit_expression(self, manager)

    # -Properties
    @property
    def is_empty(self) -> bool:
        return self._expression is None

    @property
    def expression(self) -> NodeExpr:
        assert self._expression is not None
        return self._expression

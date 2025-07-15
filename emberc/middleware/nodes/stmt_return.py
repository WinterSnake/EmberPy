##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: StmtReturn              ##
##-------------------------------##

## Imports
from typing import Any
from .core import Node, NodeExpr
from .visitor import NodeVisitor


## Classes
class NodeStmtReturn(Node):
    """
    Ember Node: Statement :: Return
    Represents an AST node of a return statement
    """

    # -Constructor
    def __init__(self, expression: NodeExpr | None) -> None:
        self._expression: NodeExpr | None = expression

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_statement_return(self)

    # -Properties
    @property
    def has_expression(self) -> bool:
        return self._expression is not None

    @property
    def expression(self) -> NodeExpr:
        assert self._expression is not None
        return self._expression

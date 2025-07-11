##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node::Statement - Expression  ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import Any
from .core import Node, NodeExpr
from .visitor import NodeVisitor
from ...location import Location


## Classes
class NodeStmtExpr(Node):
    """
    Ember Statement Node: Expression
    Represents a statement for an expression node
    """

    # -Constructor
    def __init__(self, expression: NodeExpr) -> None:
        self.expression: NodeExpr = expression

    # -Dunder Methods
    def __str__(self) -> str:
        return str(self.expression)

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_statement_expression(self)

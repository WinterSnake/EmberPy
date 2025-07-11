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
class NodeStmtIf(Node):
    """
    Ember Statement Node: Block
    Represents a statement block node
    """

    # -Constructor
    def __init__(
        self, condition: NodeExpr, body: Node, branch: Node | None
    ) -> None:
        self.condition: NodeExpr = condition
        self.body: Node = body
        self.branch: Node | None = branch

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_statement_if(self)

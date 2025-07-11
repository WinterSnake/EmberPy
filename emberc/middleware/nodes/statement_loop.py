##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node::Statement - Loop        ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import Any
from .core import Node, NodeExpr
from .visitor import NodeVisitor
from ...location import Location


## Classes
class NodeStmtLoop(Node):
    """
    Ember Statement Node: Loop
    Represents a statement for loops
    """

    # -Constructor
    def __init__(self, condition: NodeExpr, body: Node) -> None:
        self.condition: NodeExpr = condition
        self.body: Node = body

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_statement_loop(self)

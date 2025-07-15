##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: StmtLoop                ##
##-------------------------------##

## Imports
from typing import Any
from .core import Node, NodeExpr
from .visitor import NodeVisitor


## Classes
class NodeStmtLoop(Node):
    """
    Ember Node: Statement :: Loop
    Represents an AST node of a loop statement with condition and body
    """

    # -Constructor
    def __init__(self, condition: NodeExpr, body: Node) -> None:
        self.condition: NodeExpr = condition
        self.body: Node = body

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_statement_loop(self)

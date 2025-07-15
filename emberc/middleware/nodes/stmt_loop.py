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
    Ember Node: Statement :: Condition
    Represents an AST node of a if statement with
    condition, body, and branch
    """

    # -Constructor
    def __init__(self, condition: NodeExpr, body: Node) -> None:
        self.condition: NodeExpr = condition
        self.body: Node = body

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_statement_loop(self)

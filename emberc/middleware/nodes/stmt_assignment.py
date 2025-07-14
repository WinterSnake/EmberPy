##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: StmtAssignment          ##
##-------------------------------##

## Imports
from typing import Any
from .core import Node, NodeExpr
from .visitor import NodeVisitor


## Classes
class NodeStmtAssignment(Node):
    """
    Ember Node: Statement :: Assignment
    Represents an AST node of a assignment statement
    with identifier and expression
    """

    # -Constructor
    def __init__(self, _id: str, expression: NodeExpr) -> None:
        self.id: str = _id
        self.expression: NodeExpr = expression

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_statement_assignment(self)

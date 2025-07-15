##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: StmtCondition           ##
##-------------------------------##

## Imports
from typing import Any
from .core import Node, NodeExpr
from .visitor import NodeVisitor


## Classes
class NodeStmtCondition(Node):
    """
    Ember Node: Statement :: Condition
    Represents an AST node of a if statement with
    condition, body, and branch
    """

    # -Constructor
    def __init__(
        self, condition: NodeExpr, body: Node, branch: Node | None
    ) -> None:
        self.condition: NodeExpr = condition
        self.body: Node = body
        self._branch: Node | None = branch

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_statement_condition(self)

    # -Properties
    @property
    def has_branch(self) -> bool:
        return self._branch is not None

    @property
    def branch(self) -> Node:
        assert self._branch is not None
        return self._branch

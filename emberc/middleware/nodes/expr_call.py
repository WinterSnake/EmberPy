##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: ExprCall                ##
##-------------------------------##

## Imports
from collections.abc import Sequence
from typing import Any
from .core import Node, NodeExpr
from .visitor import NodeVisitor


## Classes
class NodeExprCall(NodeExpr):
    """
    Ember Node: Expression :: Call
    Represents an AST node of an expression call with arguments
    """

    # -Constructor
    def __init__(
        self, callee: NodeExpr, arguments: Sequence[NodeExpr]
    ) -> None:
        self.callee: NodeExpr = callee
        self.arguments: Sequence[NodeExpr] = arguments

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_call(self)

    # -Properties
    @property
    def argument_count(self) -> int:
        return len(self.arguments)

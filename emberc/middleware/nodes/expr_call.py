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
        self, callee: NodeExpr, arguments: Sequence[NodeExpr] | None
    ) -> None:
        self.callee: NodeExpr = callee
        self._arguments: Sequence[NodeExpr] | None = arguments

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_call(self)

    # -Properties
    @property
    def has_arguments(self) -> bool:
        if self._arguments is None:
            return False
        return True

    @property
    def arguments(self) -> Sequence[NodeExpr]:
        assert self._arguments is not None
        return self._arguments

    @property
    def argument_count(self) -> int:
        if not self.has_arguments:
            return 0
        return len(self.arguments)

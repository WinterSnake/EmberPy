##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Expression Group        ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Collection
from typing import TYPE_CHECKING
from .expr import NodeExpr
from ...location import Location

if TYPE_CHECKING:
    from ..visitor import NodeVisitor, NodeExprVisitor


## Classes
class NodeExprCall(NodeExpr):
    """
    Ember Expression Node : Call
    Represents an AST node of a function calling expression with arguments
    """

    # -Constructor
    def __init__(
        self, location: Location, callee: NodeExpr, arguments: Collection[NodeExpr]
    ) -> None:
        super().__init__(location)
        self.callee: NodeExpr = callee
        self.arguments: Collection[NodeExpr] = arguments

    # -Instance Methods
    def accept[T](self, visitor: NodeExprVisitor[T], manager: NodeVisitor) -> T:
        return visitor.visit_expr_call(self, manager)

    # -Properties
    @property
    def argument_count(self) -> int:
        return len(self.arguments)

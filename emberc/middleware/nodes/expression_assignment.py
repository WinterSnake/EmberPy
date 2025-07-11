##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node::Expression - Assignment ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import Any
from .core import NodeExpr
from .expression_literal import NodeExprId
from .visitor import NodeVisitor
from ...location import Location


## Classes
class NodeExprAssign(NodeExpr):
    """
    Ember Expression Node: Assignment
    Represents an assignment expression node for variables
    """
    # -Constructor
    def __init__(
        self, location: Location, l_value: NodeExprId, r_value: NodeExpr
    ) -> None:
        super().__init__(location)
        self.l_value: NodeExprId = l_value
        self.r_value: NodeExpr = r_value

    # -Dunder Methods
    def __str__(self) -> str:
        return f"Id({self.l_value.id}) = {self.r_value}"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_assign(self)

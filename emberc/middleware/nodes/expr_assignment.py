##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: ExprAssignment          ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import Any
from .core import Node, NodeExpr
from .visitor import NodeVisitor
from ...location import Location


## Classes
class NodeExprAssignment(NodeExpr):
    """
    Ember Node: Expression :: Assignment
    Represents an AST node of an assignment expression
    with it's l and r value nodes
    """

    # -Constructor
    def __init__(
        self, location: Location, l_value: NodeExpr, r_value: NodeExpr
    ) -> None:
        super().__init__(location)
        self.l_value: NodeExpr = l_value
        self.r_value: NodeExpr = r_value

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_assignment(self)

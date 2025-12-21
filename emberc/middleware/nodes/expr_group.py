##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Expression Group        ##
##-------------------------------##

## Imports
from __future__ import annotations
from .expr import NodeExpr
from ...location import Location


## Classes
class NodeExprGroup(NodeExpr):
    """
    Ember Expression Node : Group
    Represents an AST node of a grouped expression
    """

    # -Constructor
    def __init__(self, location: Location, expression: NodeExpr) -> None:
        super().__init__(location)
        self.expression: NodeExpr = expression

    # -Dunder Methods
    def __str__(self) -> str:
        return str(self.expression)

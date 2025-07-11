##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Expression - Logic      ##
##-------------------------------##

## Imports
from typing import Any
from .core import NodeExpr
from .visitor import NodeVisitor
from ...location import Location


## Classes
class NodeExprAssignment(NodeExpr):
    """
    Ember Node: Expression :: Assignment
    Represents an AST node of an assignment expression
    """

    # -Constructor
    def __init__(self, location: Location, _id: str, expression: NodeExpr) -> None:
        super().__init__(location)
        self.id: str = _id
        self.expression: NodeExpr = expression

    # -Dunder Methods
    def __str__(self) -> str:
        return f"(Id({self.id}) = {self.expression})"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_assignment(self)

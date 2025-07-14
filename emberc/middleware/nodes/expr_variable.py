## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: ExprVariable            ##
##-------------------------------##

## Imports
from typing import Any
from .core import NodeExpr
from .visitor import NodeVisitor
from ...location import Location


## Classes
class NodeExprVariable(NodeExpr):
    """
    Ember Node: Expression :: Variable
    Represents an AST node of a variable expression with it's id
    """

    # -Constructor
    def __init__(self, location: Location, _id: str) -> None:
        super().__init__(location)
        self.id: str = _id

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_variable(self)

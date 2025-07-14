##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: ExprGroup               ##
##-------------------------------##

## Imports
from typing import Any
from .core import Node, NodeExpr
from .visitor import NodeVisitor


## Classes
class NodeExprGroup(NodeExpr):
    """
    Ember Node: Expression :: Group
    Represents an AST node of an expression with higher precedence
    """

    # -Constructor
    def __init__(self, expression: NodeExpr) -> None:
        self.expression: NodeExpr = expression

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_group(self)

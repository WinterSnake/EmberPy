##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Statment Node: Expressions    ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .node import StmtNode

if TYPE_CHECKING:
    from . import StmtNodeVisitor
    from ..expressions import ExprNode


## Classes
@dataclass(slots=True)
class StmtExpressionNode(StmtNode):
    """
    Resolved Expression Statement
    Wraps an inner expression terminated by a semicolon.
    """
    # -Instance Methods
    def accept[T](self, visitor: StmtNodeVisitor[T]) -> T:
        return visitor.visit_expression(self)

    # -Properties
    expression: ExprNode

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Expr Node: Binary             ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import TYPE_CHECKING
from .node import ExprNode

if TYPE_CHECKING:
    from . import ExprNodeVisitor
    from ...operators import (
        AssignOperator,
        BinaryOperator,
    )


## Classes
@dataclass(slots=True)
class ExprAssignNode(ExprNode):
    """
    Resolved Assignment Expression
    Encapsulates an assignment operator along with its l-value and r-value expressions.
    """
    # -Instance Methods
    def accept[T](self, visitor: ExprNodeVisitor[T]) -> T:
        return visitor.visit_assignment(self)

    # -Properties
    operator: AssignOperator
    l_value: ExprNode
    r_value: ExprNode


@dataclass(slots=True)
class ExprBinaryNode(ExprNode):
    """
    Unresolved Binary Expression
    Encapsulates an infix arithmetic operator along with its left-hand and right-hand expressions.
    """
    # -Instance Methods
    def accept[T](self, visitor: ExprNodeVisitor[T]) -> T:
        return visitor.visit_binary(self)

    # -Properties
    operator: BinaryOperator
    lhs: ExprNode
    rhs: ExprNode

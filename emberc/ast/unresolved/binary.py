##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Binary       ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from . import UnresolvedNodeVisitor
    from ..operators import (
        AssignOperator,
        BinaryOperator,
    )
    from ...core import Span


## Classes
@dataclass(slots=True)
class UnresolvedAssignNode(UnresolvedNode):
    """
    Unresolved Assignment Expression
    Encapsulates an assignment operator along with its l-value and r-value expressions.
    """
    # -Instance Methods
    def accept[T](self, visitor: UnresolvedNodeVisitor[T]) -> T:
        return visitor.visit_assignment(self)

    # -Properties
    operator: AssignOperator
    l_value: UnresolvedNode
    r_value: UnresolvedNode

    @property
    def wide_span(self) -> Span:
        l_span = self.l_value.wide_span
        r_span = self.r_value.wide_span
        return l_span.extend_to(r_span)


@dataclass(slots=True)
class UnresolvedBinaryNode(UnresolvedNode):
    """
    Unresolved Binary Expression
    Encapsulates an infix arithmetic operator along with its left-hand and right-hand expressions.
    """
    # -Instance Methods
    def accept[T](self, visitor: UnresolvedNodeVisitor[T]) -> T:
        return visitor.visit_binary(self)

    # -Properties
    operator: BinaryOperator
    lhs: UnresolvedNode
    rhs: UnresolvedNode

    @property
    def wide_span(self) -> Span:
        l_span = self.lhs.wide_span
        r_span = self.rhs.wide_span
        return l_span.extend_to(r_span)

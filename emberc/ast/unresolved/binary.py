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
    from ..common import AssignOperator, BinaryOperator
    from ...core import Span


## Classes
@dataclass(slots=True)
class UnresolvedAssignNode(UnresolvedNode):
    """Assignment AST node with l_value and r_value nodes and the assignment operator."""
    # -Instance Methods
    def accept[R](self, visitor: UnresolvedNodeVisitor[R]) -> R:
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
    """Binary AST node with lhs and rhs nodes and the binary operator."""
    # -Instance Methods
    def accept[R](self, visitor: UnresolvedNodeVisitor[R]) -> R:
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

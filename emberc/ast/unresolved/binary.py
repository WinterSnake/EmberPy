##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved AST: Binary        ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from . import UnresolvedNodeVisitor
    from ...core import Span


## Classes
@dataclass(slots=True)
class UnresolvedAssignNode(UnresolvedNode):
    """
    An AST node representing an assignment expression.
    Encapsulates an assignment operator along with its l-value and r-value expressions.
    """
    # -Instance Methods
    def accept[T](self, visitor: UnresolvedNodeVisitor[T]) -> T:
        return visitor.visit_assignment(self)

    # -Properties
    operator: UnresolvedAssignNode.Operator
    l_value: UnresolvedNode
    r_value: UnresolvedNode

    @property
    def wide_span(self) -> Span:
        l_span = self.l_value.wide_span
        r_span = self.r_value.wide_span
        return l_span.extend_to(r_span)

    # -Sub-Classes
    class Operator(IntEnum):
        Eq = auto()


@dataclass(slots=True)
class UnresolvedBinaryNode(UnresolvedNode):
    """
    An AST node representing a binary expression.
    Encapsulates an infix arithmetic operator (e.g., addition, multiplication)
    along with its left-hand and right-hand operand expressions.
    """
    # -Instance Methods
    def accept[T](self, visitor: UnresolvedNodeVisitor[T]) -> T:
        return visitor.visit_binary(self)

    # -Properties
    operator: UnresolvedBinaryNode.Operator
    lhs: UnresolvedNode
    rhs: UnresolvedNode

    @property
    def wide_span(self) -> Span:
        l_span = self.lhs.wide_span
        r_span = self.rhs.wide_span
        return l_span.extend_to(r_span)

    # -Sub-Classes
    class Operator(IntEnum):
        Add = auto()
        Sub = auto()
        Mul = auto()
        Div = auto()
        Mod = auto()

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Unary        ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from . import UnresolvedNodeVisitor
    from ..common import UnaryOperator
    from ...core import Span


## Classes
@dataclass(slots=True)
class UnresolvedUnaryPrefixNode(UnresolvedNode):
    """Unary AST node the operand node and the unary operator."""
    # -Instance Methods
    def accept[R](self, visitor: UnresolvedNodeVisitor[R]) -> R:
        return visitor.visit_unary(self)

    # -Properties
    operator: UnaryOperator
    operand: UnresolvedNode

    @property
    def wide_span(self) -> Span:
        return self.location.extend_to(self.operand.wide_span)

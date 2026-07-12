##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Expression  ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from . import UnresolvedNodeVisitor
    from ...core import Span


## Classes
@dataclass(slots=True)
class UnresolvedExprNode(UnresolvedNode):
    """
    An AST node representing an expression statement.
    Wraps an optional inner expression terminated by a semicolon.
    """
    # -Instance Methods
    def accept[T](self, visitor: UnresolvedNodeVisitor[T]) -> T:
        return visitor.visit_expression(self)

    # -Properties
    _expression: UnresolvedNode | None

    @property
    def has_expression(self) -> bool:
        return self._expression is not None

    @property
    def expression(self) -> UnresolvedNode:
        assert self._expression is not None
        return self._expression

    @property
    def wide_span(self) -> Span:
        if not self.has_expression:
            return self.location
        return self.location.extend_from(self.expression.wide_span)


@dataclass(slots=True)
class UnresolvedGroupNode(UnresolvedNode):
    """
    An AST node representing a grouped expression.
    Wraps an inner expression to explicitly define or alter evaluation precedence.
    """
    # -Instance Methods
    def accept[T](self, visitor: UnresolvedNodeVisitor[T]) -> T:
        return visitor.visit_group(self)

    # -Properties
    inner: UnresolvedNode

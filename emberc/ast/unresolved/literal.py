##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Literal      ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import TYPE_CHECKING, Self
from .node import UnresolvedNode

if TYPE_CHECKING:
    from . import UnresolvedNodeVisitor
    from ...core import LITERAL_VALUE_TYPE, Span


## Classes
@dataclass(slots=True)
class UnresolvedLiteralNode(UnresolvedNode):
    """
    An AST node representing a literal value terminal.
    """
    # -Instance Methods
    def accept[T](self, visitor: UnresolvedNodeVisitor[T]) -> T:
        return visitor.visit_literal(self)

    def value_as[T: LITERAL_VALUE_TYPE](self, _type: type[T]) -> T:
        return self.value  # type: ignore[return-value]

    # -Class Methods
    @classmethod
    def integer(cls, location: Span, value: int) -> Self:
        return cls(location, UnresolvedLiteralNode.Kind.Integer, value)

    # -Properties
    kind: UnresolvedLiteralNode.Kind
    value: LITERAL_VALUE_TYPE

    # -Sub-Classes
    class Kind(IntEnum):
        Integer = auto()

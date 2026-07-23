##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Literal      ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from . import UnresolvedNodeVisitor

## Constants
type UnresolvedLiteralNode = UnresolvedBooleanNode | UnresolvedIntegerNode


## Classes
@dataclass(slots=True)
class UnresolvedBooleanNode(UnresolvedNode):
    """Literal Boolean AST node with value."""
    # -Instance Methods
    def accept[R](self, visitor: UnresolvedNodeVisitor[R]) -> R:
        return visitor.visit_boolean(self)

    # -Properties
    value: bool


@dataclass(slots=True)
class UnresolvedIntegerNode(UnresolvedNode):
    """Literal Integer AST node with value."""
    # -Instance Methods
    def accept[R](self, visitor: UnresolvedNodeVisitor[R]) -> R:
        return visitor.visit_integer(self)

    # -Properties
    value: int

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Declaration Node: Variable    ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .node import DeclNode

if TYPE_CHECKING:
    from . import DeclNodeVisitor
    from ..expressions import ExprNode

## Classes
@dataclass(slots=True)
class DeclVariableNode(DeclNode):
    """
    Resolved Variable Declaration
    Encapsulates the underlying symbol id and it's initializer.
    """
    # -Instance Methods
    def accept[T](self, visitor: DeclNodeVisitor[T]) -> T:
        return visitor.visit_variable(self)

    # -Properties
    id: int
    _initializer: ExprNode | None

    @property
    def has_initializer(self) -> bool:
        return self._initializer is not None

    @property
    def initializer(self) -> ExprNode:
        assert self._initializer is not None
        return self._initializer

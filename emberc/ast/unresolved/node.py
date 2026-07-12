##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved: Node              ##
##-------------------------------##

## Imports
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import MutableSequence
    from . import UnresolvedNodeVisitor
    from ...core import Span


## Classes
@dataclass(slots=True)
class UnresolvedNode(ABC):
    """The abstract base class for all unresolved AST nodes."""
    # -Instance Methods
    @abstractmethod
    def accept[T](self, visitor: UnresolvedNodeVisitor[T]) -> T: ...

    # -Properties
    location: Span

    @property
    def wide_span(self) -> Span:
        return self.location


@dataclass(slots=True)
class UnresolvedUnitNode(UnresolvedNode):
    """
    An AST node representing a top-level compilation unit.
    Acts as the root container holding a sequence of unresolved child nodes.
    """
    # -Dunder Methods
    def __iter__(self) -> Iterator[UnresolvedNode]:
        yield from self.children

    # -Instance Methods
    def accept[T](self, visitor: UnresolvedNodeVisitor[T]) -> T:
        return visitor.visit_unit(self)

    # -Properties
    children: MutableSequence[UnresolvedNode]

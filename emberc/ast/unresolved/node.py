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
    """The abstract base class for all unresolved nodes."""
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
    Unresolved Unit Declaration
    Root container node holding a sequence of top-level unresolved nodes.
    """
    # -Dunder Methods
    def __iter__(self) -> Iterator[UnresolvedNode]:
        yield from self.nodes

    # -Instance Methods
    def accept[T](self, visitor: UnresolvedNodeVisitor[T]) -> T:
        return visitor.visit_unit(self)

    # -Properties
    nodes: MutableSequence[UnresolvedNode]

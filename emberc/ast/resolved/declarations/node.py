##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Declaration: Node             ##
##-------------------------------##

## Imports
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, NoReturn

if TYPE_CHECKING:
    from collections.abc import Iterator, MutableSequence, Sequence
    from . import DeclNodeVisitor


## Classes
@dataclass(slots=True)
class DeclNode(ABC):
    """The abstract base class for all resolved declaration nodes."""
    # -Instance Methods
    @abstractmethod
    def accept[T](self, visitor: DeclNodeVisitor[T]) -> T: ...


@dataclass(slots=True)
class DeclUnitNode(DeclNode):
    """
    Resolved Unit Declaration
    Root container node holding a sequence of top-level resolved declaration nodes.
    """
    # -Dunder Methods
    def __iter__(self) -> Iterator[DeclNode]:
        yield from self.nodes

    # -Instance Methods
    def accept[T](self, visitor: DeclNodeVisitor[T]) -> T:
        return visitor.visit_unit(self)

    # -Properties
    nodes: MutableSequence[DeclNode]


@dataclass(slots=True)
class DeclSequenceNode(DeclNode):
    """
    Resolved Sequence Declaration
    Root container node holding a sequence of resolved declaration nodes.
    Internal use for flattening multi-declaration nodes.
    """
    # -Dunder Methods
    def __iter__(self) -> Iterator[DeclNode]:
        yield from self.children

    # -Instance Methods
    def accept[T](self, visitor: DeclNodeVisitor[T]) -> NoReturn:
        assert False, "Tried visiting a sequence declaration node"

    # -Properties
    children: Sequence[DeclNode]

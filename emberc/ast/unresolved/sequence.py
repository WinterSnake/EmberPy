##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Sequence     ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from collections.abc import Iterator, MutableSequence
    from . import UnresolvedNodeVisitor


## Classes
@dataclass(slots=True)
class UnresolvedSequenceNode(UnresolvedNode):
    """Internal iterable sequence AST node."""
    # -Dunder Methods
    def __iter__(self) -> Iterator[UnresolvedNode]:
        yield from self.nodes

    def __len__(self) -> int:
        return len(self.nodes)

    # -Properties
    nodes: MutableSequence[UnresolvedNode]


@dataclass(slots=True)
class UnresolvedUnitNode(UnresolvedSequenceNode):
    """Unit AST node with all declaration nodes."""
    # -Instance Methods
    def accept[R](self, visitor: UnresolvedNodeVisitor[R]) -> R:
        return visitor.visit_unit(self)


@dataclass(slots=True)
class UnresolvedBlockNode(UnresolvedSequenceNode):
    """Block AST node with all children nodes."""
    # -Instance Methods
    def accept[R](self, visitor: UnresolvedNodeVisitor[R]) -> R:
        return visitor.visit_block(self)

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Variable     ##
##-------------------------------##

## Imports
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence
    from . import UnresolvedNodeVisitor
    from ...core import Span


## Classes
@dataclass(slots=True)
class UnresolvedIdentifierNode(UnresolvedNode):
    """Identifier AST node with name and bound id."""
    # -Instance Methods
    def accept[R](self, visitor: UnresolvedNodeVisitor[R]) -> R:
        return visitor.visit_identifier(self)

    # -Properties
    name: str
    _id: int | None = field(default=None, init=False)

    @property
    def has_id(self) -> bool:
        '''Return if id has been assigned to node.'''
        return self._id is not None

    @property
    def id(self) -> int:
        '''Return id of node; assert id exists.'''
        assert self._id is not None
        return self._id


@dataclass(slots=True)
class UnresolvedVariableNode(UnresolvedNode):
    """Variable Declaration AST node with type and collection of defined variable entries."""
    # -Dunder Methods
    def __iter__(self) -> Iterator[UnresolvedVariableNode.Entry]:
        yield from self.entries

    # -Instance Methods
    def accept[R](self, visitor: UnresolvedNodeVisitor[R]) -> R:
        return visitor.visit_variable(self)

    # -Properties
    type: UnresolvedNode
    entries: Sequence[UnresolvedVariableNode.Entry]

    @property
    def wide_span(self) -> Span:
        return self.type.wide_span.extend_to(self.location)

    # -Sub-Classes
    @dataclass(slots=True)
    class Entry:
        """Variable entry with associated name, id, and initialzier."""
        # -Properties
        location: Span
        name: str
        _initializer: UnresolvedNode | None
        _id: int | None = field(default=None, init=False)

        @property
        def has_id(self) -> bool:
            '''Return if id has been assigned to entry.'''
            return self._id is not None

        @property
        def id(self) -> int:
            '''Return id of entry; assert id exists.'''
            assert self._id is not None
            return self._id

        @property
        def has_initializer(self) -> bool:
            '''Return if entry has initializer node.'''
            return self._initializer is not None

        @property
        def initializer(self) -> UnresolvedNode:
            '''Return initializer node; assert node exists.'''
            assert self._initializer is not None
            return self._initializer

        @property
        def wide_span(self) -> Span:
            if not self.has_initializer:
                return self.location
            return self.location.extend_to(self.initializer.location)

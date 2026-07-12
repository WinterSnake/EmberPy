##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Variable     ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence
    from . import UnresolvedNodeVisitor
    from ...core import Span


## Classes
@dataclass(slots=True)
class UnresolvedIdentifierNode(UnresolvedNode):
    """
    Unresolved Identifier
    Represents an identifier token node without full context of being a name or expression.
    """
    # -Instance Methods
    def accept[T](self, visitor: UnresolvedNodeVisitor[T]) -> T:
        return visitor.visit_identifier(self)

    # -Properties
    name: str
    _id: int | None = None

    @property
    def has_id(self) -> bool:
        return self._id is not None

    @property
    def id(self) -> int:
        assert self._id is not None
        return self._id


@dataclass(slots=True)
class UnresolvedVariableNode(UnresolvedNode):
    """
    Unresolved Variable Declaration
    Encapsulates the underlying type and a sequence of declared variable entries.
    """
    # Dunder Methods
    def __iter__(self) -> Iterator[UnresolvedVariableNode.Entry]:
        yield from self.entries

    # -Instance Methods
    def accept[T](self, visitor: UnresolvedNodeVisitor[T]) -> T:
        return visitor.visit_variable(self)

    # -Properties
    type: UnresolvedNode
    entries: Sequence[UnresolvedVariableNode.Entry]

    # -Sub-Classes
    @dataclass(slots=True)
    class Entry:
        '''
        Variable Declaration Entry
        Encapsulates the variable name, an optional initializer expression.
        '''
        # -Properties
        location: Span
        name: str
        _initializer: UnresolvedNode | None
        _id: int | None = None

        @property
        def has_id(self) -> bool:
            return self._id is not None

        @property
        def id(self) -> int:
            assert self._id is not None
            return self._id

        @property
        def has_initializer(self) -> bool:
            return self._initializer is not None

        @property
        def initializer(self) -> UnresolvedNode:
            assert self._initializer is not None
            return self._initializer

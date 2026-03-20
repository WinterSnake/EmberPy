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
    from ...core import Location, MutableCollection


## Classes
@dataclass
class UnresolvedEnumNode(UnresolvedNode):
    """
    Unresolved AST Node: Enum

    A declaration node representing an enum collection and it's optional type
    """
    # -Properties
    name: str
    _id: int | None = field(init=False, default=None)
    _type: UnresolvedNode | None
    entries: MutableCollection[UnresolvedEnumNode.Entry]

    @property
    def has_id(self) -> bool:
        return self._id is not None

    @property
    def id(self) -> int:
        assert self._id is not None
        return self._id

    @property
    def has_type(self) -> bool:
        return self._type is not None

    @property
    def type(self) -> UnresolvedNode:
        assert self._type is not None
        return self._type

    # -Sub-Classes
    @dataclass
    class Entry:
        '''Meta-data for enum entries'''
        # -Properties
        location: Location
        name: str
        _id: int | None = field(init=False, default=None)
        _initializer: UnresolvedNode | None

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

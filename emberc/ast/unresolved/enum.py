##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Enum         ##
##-------------------------------##

## Imports
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from ...core import Location, MutableCollection

## Constants
type ENUM_ENTRY_TYPES = UnresolvedNode | MutableCollection[UnresolvedEnumNode.Tag]


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
    is_union: bool
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
        # -Instance Methods
        def value_as[T: ENUM_ENTRY_TYPES](self, _type: type[T]) -> T:
            assert type(self.value) is _type, "TODO: Error handling"
            return self.value

        # -Properties
        location: Location
        name: str
        _id: int | None = field(init=False, default=None)
        _value: ENUM_ENTRY_TYPES | None

        @property
        def has_id(self) -> bool:
            return self._id is not None

        @property
        def id(self) -> int:
            assert self._id is not None
            return self._id

        @property
        def has_value(self) -> bool:
            return self._value is not None

        @property
        def value(self) -> ENUM_ENTRY_TYPES:
            assert self._value is not None
            return self._value

    @dataclass
    class Tag:
        '''Meta-data for enum tagged union'''
        # -Properties
        type: UnresolvedNode
        name: str
        _id: int | None = field(init=False, default=None)

        @property
        def has_id(self) -> bool:
            return self._id is not None

        @property
        def id(self) -> int:
            assert self._id is not None
            return self._id

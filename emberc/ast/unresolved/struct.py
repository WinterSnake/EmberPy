##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Struct       ##
##-------------------------------##

## Imports
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from ...core import Location, MutableCollection

## Constants
type STRUCT_FIELD_TYPES = UnresolvedStructNode | UnresolvedStructNode.Field


## Classes
@dataclass
class UnresolvedStructNode(UnresolvedNode):
    """
    Unresolved AST Node: Struct

    A declaration node representing an struct and it's fields.
    """
    # -Properties
    name: str
    _id: int | None = field(init=False, default=None)
    members: MutableCollection[STRUCT_FIELD_TYPES]
    is_union: bool = False

    @property
    def has_id(self) -> bool:
        return self._id is not None

    @property
    def id(self) -> int:
        assert self._id is not None
        return self._id

    # -Sub-Classes
    @dataclass
    class Field:
        '''Meta-data for struct fields'''
        # -Properties
        type: UnresolvedNode
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

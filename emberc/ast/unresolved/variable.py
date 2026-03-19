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
    from typing import MutableSequence
    from ...core import Location


## Classes
@dataclass
class UnresolvedVariableNode(UnresolvedNode):
    """
    Unresolved AST Node: Variable

    A declaration node representing one or more variables sharing a master type.
    """
    # -Properties
    type: UnresolvedNode
    entries: MutableSequence[UnresolvedVariableNode.Entry]

    # -Sub-Classes
    @dataclass
    class Entry:
        '''Meta-data for variable entries'''
        # -Properties
        location: Location
        name: str
        _initializer: UnresolvedNode | None
        _id: int | None = field(init=False, default=None)

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

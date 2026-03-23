##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type Node: Identifier         ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar
from .core import TypeNode

if TYPE_CHECKING:
    from typing import Self


## Classes
@dataclass(frozen=True, slots=True)
class IdentifierTypeNode(TypeNode):
    """
    Resolved Type Node: Identifier

    A reference to a user-defined type; links type usage to type's symbol id.
    """
    # -Class Methods
    @classmethod
    def from_id(cls, _id: int) -> Self:
        '''Get or create an identifier type node from an id'''
        if _id not in cls._mapped_ids:
            cls._mapped_ids[_id] = cls(_id)
        return cls._mapped_ids[_id]

    # -Properties
    id: int

    # -Class Properties
    _mapped_ids: ClassVar[dict[int, Self]] = {}

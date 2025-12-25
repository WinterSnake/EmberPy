##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type Node: Identifier         ##
##-------------------------------##

## Imports
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Self
from .base import NodeType


## Classes
@dataclass(frozen=True, slots=True)
class NodeTypeIdentifier(NodeType):
    """
    Ember Type: Identifier

    A type representing a bound identifier
    used for lookups to what identity represents

    Uses a cache map to store single instances
    """

    # -Class Methods
    @classmethod
    def from_id(cls, _id: int) -> Self:
        '''Create or get an identifier type instance from an id'''
        if _id not in cls._mapped_ids:
            cls._mapped_ids[_id] = cls(_id)
        return cls._mapped_ids[_id]

    # -Properties
    id: int

    # -Class Properties
    _mapped_ids: ClassVar[dict[int, Self]] = {}

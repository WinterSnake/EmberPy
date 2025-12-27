##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type Node: Identifier         ##
##-------------------------------##

## Imports
from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ClassVar, Self
from .base import NodeType

if TYPE_CHECKING:
    from .visitor import NodeTypeVisitor
    from ...unresolved import UnresolvedNodeVisitor


## Classes
@dataclass(frozen=True, slots=True)
class NodeTypeIdentifier(NodeType):
    """
    Ember Type: Identifier

    A type representing a bound identifier
    used for lookups to what type id represents

    Uses a cache map to store single instances
    """
    # -Instance Methods
    def accept[T](self, visitor: NodeTypeVisitor[T]) -> T:
        return visitor.visit_type_identifier(self)

    def bind[T](self, visitor: UnresolvedNodeVisitor[T]) -> None: ...

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

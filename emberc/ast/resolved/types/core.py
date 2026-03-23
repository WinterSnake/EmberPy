##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolved Node: Type           ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from ..node import ResolvedNode


## Classes
class TypeNode(ResolvedNode):
    """
    Resolved AST Node: Type

    A representation for typed nodes within the Ember language.
    """
    pass


@dataclass(frozen=True, slots=True)
class PendingTypeNode(TypeNode):
    """
    Resolved Type Node: Pending

    Represents a type whose concrete identity or memory constraints
    are currently unknown. Can also be used as an inferred parent linked type.
    """
    # -Properties
    _parent_id: int | None = None

    @property
    def has_parent_id(self) -> bool:
        return self._parent_id is not None

    @property
    def parent_id(self) -> int:
        assert self._parent_id is not None
        return self._parent_id

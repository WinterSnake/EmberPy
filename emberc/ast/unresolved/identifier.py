##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Identifier   ##
##-------------------------------##

## Imports
from dataclasses import dataclass, field
from .node import UnresolvedNode


## Classes
@dataclass
class UnresolvedIdentifierNode(UnresolvedNode):
    """
    Unresolved AST Node: Identifier

    A leaf container for holding an identifier and it's id.
    """
    # -Properties
    name: str
    _id: int | None = field(init=False, default=None)

    @property
    def has_id(self) -> bool:
        return self._id is not None

    @property
    def id(self) -> int:
        assert self._id is not None
        return self._id

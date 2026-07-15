##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Type         ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import TYPE_CHECKING, assert_never
from .node import UnresolvedNode

if TYPE_CHECKING:
    from . import UnresolvedNodeVisitor


## Classes
@dataclass(slots=True)
class UnresolvedTypeNode(UnresolvedNode):
    """
    Unresolved Primitive Type
    Encapsulates the specific kind of built-in data type.
    """
    # -Dunder Methods
    def __str__(self) -> str:
        match self.kind:
            case UnresolvedTypeNode.Kind.Int32:
                return "int32"
            case _:
                assert_never(self.kind)

    # -Instance Methods
    def accept[T](self, visitor: UnresolvedNodeVisitor[T]) -> T:
        return visitor.visit_type(self)

    # -Properties
    kind: UnresolvedTypeNode.Kind

    # -Sub-Classes
    class Kind(IntEnum):
        Int32 = auto()

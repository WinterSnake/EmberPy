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
            case UnresolvedTypeNode.Kind.Int8:
                return "int8"
            case UnresolvedTypeNode.Kind.Int16:
                return "int16"
            case UnresolvedTypeNode.Kind.Int32:
                return "int32"
            case UnresolvedTypeNode.Kind.Int64:
                return "int64"
            case UnresolvedTypeNode.Kind.UInt8:
                return "uint8"
            case UnresolvedTypeNode.Kind.UInt16:
                return "uint16"
            case UnresolvedTypeNode.Kind.UInt32:
                return "uint32"
            case UnresolvedTypeNode.Kind.UInt64:
                return "uint64"
            case _:
                assert_never(self.kind)

    # -Instance Methods
    def accept[T](self, visitor: UnresolvedNodeVisitor[T]) -> T:
        return visitor.visit_type(self)

    # -Properties
    kind: UnresolvedTypeNode.Kind

    # -Sub-Classes
    class Kind(IntEnum):
        Int8 = auto()
        Int16 = auto()
        Int32 = auto()
        Int64 = auto()
        UInt8 = auto()
        UInt16 = auto()
        UInt32 = auto()
        UInt64 = auto()

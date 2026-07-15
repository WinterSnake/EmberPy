##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type Node: Primitive          ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import TYPE_CHECKING, ClassVar, Self, assert_never
from .node import TypeNode

if TYPE_CHECKING:
    from . import TypeNodeVisitor


## Classes
@dataclass(frozen=True, slots=True)
class TypePrimitive(TypeNode):
    """
    Resolved Primitive Type
    Represents a built-in primitive type.
    """
    # -Dunder Methods
    def __str__(self) -> str:
        match self.kind:
            case TypePrimitive.Kind.Int8:
                return "int8"
            case TypePrimitive.Kind.Int16:
                return "int16"
            case TypePrimitive.Kind.Int32:
                return "int32"
            case TypePrimitive.Kind.Int64:
                return "int64"
            case TypePrimitive.Kind.UInt8:
                return "uint8"
            case TypePrimitive.Kind.UInt16:
                return "uint16"
            case TypePrimitive.Kind.UInt32:
                return "uint32"
            case TypePrimitive.Kind.UInt64:
                return "uint64"
            case _:
                assert_never(self.kind)

    # -Instance Methods
    def accept[T](self, visitor: TypeNodeVisitor[T]) -> T:
        return visitor.visit_type_primitive(self)

    # -Properties
    kind: TypePrimitive.Kind

    # -Class Properties
    int8: ClassVar[Self]
    int16: ClassVar[Self]
    int32: ClassVar[Self]
    int64: ClassVar[Self]
    uint8: ClassVar[Self]
    uint16: ClassVar[Self]
    uint32: ClassVar[Self]
    uint64: ClassVar[Self]

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


## Body
TypePrimitive.int8 = TypePrimitive(TypePrimitive.Kind.Int8)
TypePrimitive.int16 = TypePrimitive(TypePrimitive.Kind.Int16)
TypePrimitive.int32 = TypePrimitive(TypePrimitive.Kind.Int32)
TypePrimitive.int64 = TypePrimitive(TypePrimitive.Kind.Int64)
TypePrimitive.uint8 = TypePrimitive(TypePrimitive.Kind.UInt8)
TypePrimitive.uint16 = TypePrimitive(TypePrimitive.Kind.UInt16)
TypePrimitive.uint32 = TypePrimitive(TypePrimitive.Kind.UInt32)
TypePrimitive.uint64 = TypePrimitive(TypePrimitive.Kind.UInt64)

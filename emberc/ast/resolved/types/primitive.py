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
            case TypePrimitive.Kind.Int32:
                return "int32"
            case _:
                assert_never(self.kind)

    # -Instance Methods
    def accept[T](self, visitor: TypeNodeVisitor[T]) -> T:
        return visitor.visit_type_primitive(self)

    # -Properties
    kind: TypePrimitive.Kind

    # -Class Properties
    int32: ClassVar[Self]

    # -Sub-Classes
    class Kind(IntEnum):
        Int32 = auto()


## Body
TypePrimitive.int32 = TypePrimitive(TypePrimitive.Kind.Int32)

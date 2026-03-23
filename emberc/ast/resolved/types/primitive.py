##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type Node: Primitive          ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar
from .core import TypeNode

if TYPE_CHECKING:
    from typing import Self


## Classes
@dataclass(frozen=True, slots=True)
class PrimitiveTypeNode(TypeNode):
    """
    Resolved Type Node: Primitive

    Represents core types built into the language.
    """
    # -Dunder Methods
    def __str__(self) -> str:
        return self.name

    # -Properties
    name: str

    # -Class Properties
    void: ClassVar[Self]
    boolean: ClassVar[Self]
    int8: ClassVar[Self]
    int16: ClassVar[Self]
    int32: ClassVar[Self]
    int64: ClassVar[Self]
    uint8: ClassVar[Self]
    uint16: ClassVar[Self]
    uint32: ClassVar[Self]
    uint64: ClassVar[Self]
    ssize: ClassVar[Self]
    usize: ClassVar[Self]
    function: ClassVar[Self]


## Body
PrimitiveTypeNode.void = PrimitiveTypeNode("void")
PrimitiveTypeNode.boolean = PrimitiveTypeNode("boolean")
PrimitiveTypeNode.int8 = PrimitiveTypeNode("int8")
PrimitiveTypeNode.int16 = PrimitiveTypeNode("int16")
PrimitiveTypeNode.int32 = PrimitiveTypeNode("int32")
PrimitiveTypeNode.int64 = PrimitiveTypeNode("int64")
PrimitiveTypeNode.uint8 = PrimitiveTypeNode("uint8")
PrimitiveTypeNode.uint16 = PrimitiveTypeNode("uint16")
PrimitiveTypeNode.uint32 = PrimitiveTypeNode("uint32")
PrimitiveTypeNode.uint64 = PrimitiveTypeNode("uint64")
PrimitiveTypeNode.ssize = PrimitiveTypeNode("ssize")
PrimitiveTypeNode.usize = PrimitiveTypeNode("usize")
PrimitiveTypeNode.function = PrimitiveTypeNode("fn")

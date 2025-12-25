##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type Node: Primitive          ##
##-------------------------------##

## Imports
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, Self
from .base import NodeType


## Classes
@dataclass(frozen=True, slots=True)
class NodeTypePrimitive(NodeType):
    """
    Ember Type: Primitive

    A type representing the prititive and core types to the language
    """
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


## Body
NodeTypePrimitive.void = NodeTypePrimitive()
NodeTypePrimitive.boolean = NodeTypePrimitive()
NodeTypePrimitive.int8 = NodeTypePrimitive()
NodeTypePrimitive.int16 = NodeTypePrimitive()
NodeTypePrimitive.int32 = NodeTypePrimitive()
NodeTypePrimitive.int64 = NodeTypePrimitive()
NodeTypePrimitive.uint8 = NodeTypePrimitive()
NodeTypePrimitive.uint16 = NodeTypePrimitive()
NodeTypePrimitive.uint32 = NodeTypePrimitive()
NodeTypePrimitive.uint64 = NodeTypePrimitive()

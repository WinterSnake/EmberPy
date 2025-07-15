##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Datatype                      ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from ..frontend.token import Token


## Functions
def get_datatype_from_token(_type: Token.Type) -> Datatype:
    """Returns a datatype associated with a typed keyword"""
    match _type:
        case Token.Type.KeywordVoid:
            return Datatype.Void
        case Token.Type.KeywordBoolean:
            return Datatype.Boolean
        case Token.Type.KeywordInt8:
            return Datatype.Int8
        case Token.Type.KeywordInt16:
            return Datatype.Int16
        case Token.Type.KeywordInt32:
            return Datatype.Int32
        case Token.Type.KeywordInt64:
            return Datatype.Int64
        case Token.Type.KeywordUInt8:
            return Datatype.UInt8
        case Token.Type.KeywordUInt16:
            return Datatype.UInt16
        case Token.Type.KeywordUInt32:
            return Datatype.UInt32
        case Token.Type.KeywordUInt64:
            return Datatype.UInt64
        case _:
            assert False


## Classes
class Datatype(IntEnum):
    Empty = auto()
    Void = auto()
    Boolean = auto()
    Int8 = auto()
    Int16 = auto()
    Int32 = auto()
    Int64 = auto()
    UInt8 = auto()
    UInt16 = auto()
    UInt32 = auto()
    UInt64 = auto()

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Token                         ##
##-------------------------------##

## Imports
from __future__ import annotations
from pathlib import Path
from enum import IntEnum, auto
from ..location import Location


## Classes
class Token:
    """Ember Token"""

    # -Constructor
    def __init__(
        self, location: Location, _type: Token.Type, value: str | None = None
    ) -> None:
        self.location: Location = location
        self.type: Token.Type = _type
        self.value: str | None = value

    # -Dunder Methods
    def __str__(self) -> str:
        _str = f"[{self.location}] {self.type.name}"
        if self.value:
            _str += f" '{self.value}'"
        return _str

    # -Sub-Classes
    class Type(IntEnum):
        '''Token Value Type'''
        # -Literals
        Identifier = auto()
        Integer = auto()
        # -Keywords
        If = auto()
        # -Keywords: Types
        Int8 = auto()
        Int16 = auto()
        Int32 = auto()
        Int64 = auto()
        UInt8 = auto()
        UInt16 = auto()
        UInt32 = auto()
        UInt64 = auto()
        # -Symbols
        Eq = auto()
        Bang = auto()
        Plus = auto()
        Minus = auto()
        Star = auto()
        FSlash = auto()
        Percent = auto()
        # -Symbols: Comparison
        EqEq = auto()
        BangEq = auto()
        Lt = auto()
        Gt = auto()
        LtEq = auto()
        GtEq = auto()
        # -Symbols: Misc
        LParen = auto()
        RParen = auto()
        LBrace = auto()
        RBrace = auto()
        Semicolon = auto()

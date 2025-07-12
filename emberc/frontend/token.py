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
        LiteralTrue = auto()
        LiteralFalse = auto()
        # -Keywords
        KeywordFunction = auto()
        KeywordReturn = auto()
        KeywordIf = auto()
        KeywordElse = auto()
        KeywordWhile = auto()
        KeywordDo = auto()
        KeywordFor = auto()
        # -Keywords: Types
        KeywordVoid = auto()
        KeywordBoolean = auto()
        KeywordInt8 = auto()
        KeywordInt16 = auto()
        KeywordInt32 = auto()
        KeywordInt64 = auto()
        KeywordUInt8 = auto()
        KeywordUInt16 = auto()
        KeywordUInt32 = auto()
        KeywordUInt64 = auto()
        # -Symbols
        SymbolEq = auto()
        SymbolBang = auto()
        SymbolPlus = auto()
        SymbolMinus = auto()
        SymbolStar = auto()
        SymbolFSlash = auto()
        SymbolPercent = auto()
        # -Symbols: Comparison
        SymbolEqEq = auto()
        SymbolBangEq = auto()
        SymbolLt = auto()
        SymbolGt = auto()
        SymbolLtEq = auto()
        SymbolGtEq = auto()
        # -Symbols: Misc
        SymbolLParen = auto()
        SymbolRParen = auto()
        SymbolLBrace = auto()
        SymbolRBrace = auto()
        SymbolComma = auto()
        SymbolColon = auto()
        SymbolSemicolon = auto()

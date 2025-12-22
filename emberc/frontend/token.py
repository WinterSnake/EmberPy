##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Token               ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from ..location import Location


## Classes
class Token:
    """Ember Language Token"""

    # -Constructor
    def __init__(
        self, location: Location, _type: Token.Type,
        value: int | str | None = None
    ) -> None:
        self.location: Location = location
        self.type: Token.Type = _type
        self._value: int | str | None = value

    # -Dunder Methods
    def __str__(self) -> str:
        _str = f"[{self.location}]{self.type.name}"
        if self._value is not None:
            _str += f"({self.value})"
        return _str

    # -Properties
    @property
    def value(self) -> int | str:
        assert self._value is not None
        return self._value

    # -Sub-Classes
    class Type(IntEnum):
        # -Literal
        Identifier = auto()
        Integer = auto()
        BooleanTrue = auto()
        BooleanFalse = auto()
        # -Keyword
        KeywordIf = auto()
        KeywordElse = auto()
        KeywordWhile = auto()
        KeywordDo = auto()
        KeywordFor = auto()
        KeywordFn = auto()
        KeywordReturn = auto()
        # -Keyword: Types
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
        # -Symbol: Operator
        SymbolEq = auto()
        SymbolBang = auto()
        SymbolPlus = auto()
        SymbolMinus = auto()
        SymbolStar = auto()
        SymbolFSlash = auto()
        SymbolPercent = auto()
        SymbolEqEq = auto()
        SymbolNtEq = auto()
        SymbolLt = auto()
        SymbolGt = auto()
        SymbolLtEq = auto()
        SymbolGtEq = auto()
        # -Symbol: Misc
        SymbolComma = auto()
        SymbolLParen = auto()
        SymbolRParen = auto()
        SymbolLBrace = auto()
        SymbolRBrace = auto()
        SymbolColon = auto()
        SymbolSemicolon = auto()

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Token               ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import TYPE_CHECKING
from ..location import Location

if TYPE_CHECKING:
    from ..ast import LITERAL_VALUE


## Classes
class Token:
    """Ember Language Token"""

    # -Constructor
    def __init__(
        self, location: Location, _type: Token.Type,
        value: LITERAL_VALUE | None = None
    ) -> None:
        self.location: Location = location
        self.type: Token.Type = _type
        self._value: LITERAL_VALUE | None = value

    # -Dunder Methods
    def __str__(self) -> str:
        _str = self.type.name
        if self._value is not None:
            _str += f"({self.value})"
        return _str

    # -Properties
    @property
    def value(self) -> LITERAL_VALUE:
        assert self._value is not None
        return self._value

    # -Sub-Classes
    class Type(IntEnum):
        # -Literal
        Identifier = auto()
        Boolean = auto()
        Integer = auto()
        String = auto()
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
        # -Keyword: Type Modifiers
        KeywordConst = auto()
        # -Symbol: Math
        SymbolEq = auto()
        SymbolBang = auto()
        SymbolPlus = auto()
        SymbolPlusEq = auto()
        SymbolMinus = auto()
        SymbolMinusEq = auto()
        SymbolStar = auto()
        SymbolStarEq = auto()
        SymbolFSlash = auto()
        SymbolFSlashEq = auto()
        SymbolPercent = auto()
        SymbolPercentEq = auto()
        # -Symbol: Bitwise
        SymbolBitNeg = auto()
        SymbolBitNegEq = auto()
        SymbolBitXor = auto()
        SymbolBitXorEq = auto()
        SymbolBitAnd = auto()
        SymbolBitAndEq = auto()
        SymbolBitOr = auto()
        SymbolBitOrEq = auto()
        SymbolLShift = auto()
        SymbolLShiftEq = auto()
        SymbolRShift = auto()
        SymbolRShiftEq = auto()
        # -Symbol: Comparison
        SymbolLogOr = auto()
        SymbolLogAnd = auto()
        SymbolEqEq = auto()
        SymbolNtEq = auto()
        SymbolLt = auto()
        SymbolGt = auto()
        SymbolLtEq = auto()
        SymbolGtEq = auto()
        # -Symbol: Misc
        SymbolDot = auto()
        SymbolDotDot = auto()
        SymbolComma = auto()
        SymbolColon = auto()
        SymbolSemicolon = auto()
        SymbolAt = auto()
        SymbolLParen = auto()
        SymbolRParen = auto()
        SymbolLBracket = auto()
        SymbolRBracket = auto()
        SymbolLBrace = auto()
        SymbolRBrace = auto()

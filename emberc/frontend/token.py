##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Token               ##
##-------------------------------##

## Imports
from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core import Location
    from ..ast import AST_LITERAL_TYPES

## Classes
@dataclass(frozen=True, slots=True)
class Token:
    """
    Ember Lexical Symbol

    An atomic representation of a language primitive,
    pairing a type with its value and source location.
    """
    # -Instance Methods
    def value_as[T: AST_LITERAL_TYPES](self, _type: type[T]) -> T:
        assert type(self.value) is _type, "TODO: Error handling"
        return self.value

    # -Properties
    location: Location
    type: Token.Type
    _value: AST_LITERAL_TYPES | None = None

    @property
    def has_value(self) -> bool:
        return self._value is not None

    @property
    def value(self) -> AST_LITERAL_TYPES:
        assert self._value is not None, "TODO: Error handling"
        return self._value

    # -Sub-Classes
    class Type(IntEnum):
        # -Literal
        Identifier = auto()
        Boolean = auto()
        Integer = auto()
        # -Keyword
        KeywordOr = auto()
        KeywordAnd = auto()
        KeywordIf = auto()
        KeywordElse = auto()
        KeywordWhile = auto()
        KeywordDo = auto()
        KeywordFor = auto()
        KeywordFn = auto()
        KeywordContinue = auto()
        KeywordBreak = auto()
        KeywordReturn = auto()
        # -Keyword: Type
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
        # -Keyword: Type Modifier
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

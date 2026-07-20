##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Token               ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core import Span


## Constants
type LITERAL_TYPES = bool | int | str


## Classes
@dataclass(frozen=True, slots=True)
class Token:
    """Language primitive with it's associated location, kind, and value."""
    # -Instance Methods
    def value_as[T: LITERAL_TYPES](self, _type: type[T]) -> T:
        '''Return value as type-casted literal type; assert value is of type.'''
        assert isinstance(self.value, _type)
        return self.value

    # -Properties
    span: Span
    kind: Token.Kind
    _value: LITERAL_TYPES | None

    @property
    def value(self) -> LITERAL_TYPES:
        '''Return value as generic literal type; assert value exists.'''
        assert self._value is not None
        return self._value

    # -Sub-Classes
    class Kind(IntEnum):
        # -Literals
        Boolean = auto()
        Integer = auto()
        Identifier = auto()
        # -Keywords
        KeywordIf = auto()
        KeywordElse = auto()
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
        KeywordISize = auto()
        KeywordUSize = auto()
        # -Symbols: Math
        SymbolPlus = auto()
        SymbolMinus = auto()
        SymbolStar = auto()
        SymbolFSlash = auto()
        SymbolPercent = auto()
        # -Symbols: Assignment
        SymbolEq = auto()
        # -Symbols: Comparison
        SymbolBang = auto()
        SymbolEqEq = auto()
        SymbolBangEq = auto()
        SymbolLt = auto()
        SymbolLtEq = auto()
        SymbolGt = auto()
        SymbolGtEq = auto()
        # -Symbols: Misc
        SymbolComma = auto()
        SymbolSemicolon = auto()
        SymbolLParen = auto()
        SymbolRParen = auto()
        SymbolLBrace = auto()
        SymbolRBrace = auto()

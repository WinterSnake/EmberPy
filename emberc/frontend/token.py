##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Token               ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from enum import IntEnum, auto
from ..core import LITERAL_VALUE_TYPE, Span


## Classes
@dataclass(frozen=True, slots=True)
class Token:
    """
    An Ember lexical token representing a single atomic unit of source code.
    Encapsulates its syntax kind, source text span, and optional underlying value.
    """
    # -Instance Methods
    def value_as[T: LITERAL_VALUE_TYPE](self, _type: type[T]) -> T:
        return self.value  # type: ignore[return-value]

    # -Properties
    span: Span
    kind: Token.Kind
    _value: LITERAL_VALUE_TYPE | None = None

    @property
    def has_value(self) -> bool:
        return self._value is not None

    @property
    def value(self) -> LITERAL_VALUE_TYPE:
        assert self._value is not None
        return self._value

    # -Sub-Classes
    class Kind(IntEnum):
        # -Literals
        Identifier = auto()
        Integer = auto()
        # -Keywords
        # -Keyword: Types
        KeywordInt8 = auto()
        KeywordInt16 = auto()
        KeywordInt32 = auto()
        KeywordInt64 = auto()
        KeywordUInt8 = auto()
        KeywordUInt16 = auto()
        KeywordUInt32 = auto()
        KeywordUInt64 = auto()
        # -Symbols: Math
        SymbolEq = auto()
        SymbolPlus = auto()
        SymbolMinus = auto()
        SymbolStar = auto()
        SymbolFSlash = auto()
        SymbolPercent = auto()
        # -Symbols: Misc
        SymbolComma = auto()
        SymbolSemicolon = auto()
        SymbolLParen = auto()
        SymbolRParen = auto()

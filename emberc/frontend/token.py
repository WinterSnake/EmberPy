##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Token                         ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from ..location import Location


## Functions
def get_token_repr(token: Token) -> str:
    """Returns a str that represents the type or value of given Token"""
    match token.type:
        # -Literal
        case Token.Type.Identifier:
            return token.value
        case Token.Type.Integer:
            return token.value
        # -Keyword
        case Token.Type.KeywordFunction:
            return "fn"
        # -Keyword: Type
        case Token.Type.KeywordVoid:
            return "void"
        case Token.Type.KeywordInt8:
            return "int8"
        # -Symbol: Operator
        case Token.Type.SymbolEq:
            return '='
        case Token.Type.SymbolPlus:
            return '+'
        case Token.Type.SymbolMinus:
            return '-'
        case Token.Type.SymbolStar:
            return '*'
        case Token.Type.SymbolFSlash:
            return '/'
        case Token.Type.SymbolPercent:
            return '%'
        # -Symbol: Misc
        case Token.Type.SymbolLParen:
            return '('
        case Token.Type.SymbolRParen:
            return ')'
        case Token.Type.SymbolLBrace:
            return '}'
        case Token.Type.SymbolRBrace:
            return '{'
        case Token.Type.SymbolColon:
            return ':'
        case Token.Type.SymbolSemicolon:
            return ';'


## Classes
class Token:
    """Ember Token"""

    # -Constructor
    def __init__(
        self, location: Location, _type: Token.Type,
        value: str | None = None
    ) -> None:
        self.location: Location = location
        self.type: Token.Type = _type
        self._value: str | None = value

    # -Dunder Methods
    def __str__(self) -> str:
        _str = f"[{self.location}]{self.type.name}"
        if self._value:
            _str += f"({self.value})"
        return _str

    # -Property
    @property
    def value(self) -> str:
        assert self._value is not None
        return self._value

    # -Sub-Classes
    class Type(IntEnum):
        # -Literal
        Identifier = auto()
        Integer = auto()
        # -Keyword
        KeywordFunction = auto()
        # -Keyword: Type
        KeywordVoid = auto()
        KeywordInt8 = auto()
        # -Symbol: Operator
        SymbolEq = auto()
        SymbolPlus = auto()
        SymbolMinus = auto()
        SymbolStar = auto()
        SymbolFSlash = auto()
        SymbolPercent = auto()
        # -Symbol: Misc
        SymbolLParen = auto()
        SymbolRParen = auto()
        SymbolLBrace = auto()
        SymbolRBrace = auto()
        SymbolColon = auto()
        SymbolSemicolon = auto()

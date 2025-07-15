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
        case Token.Type.KeywordTrue:
            return "true"
        case Token.Type.KeywordFalse:
            return "false"
        # -Keyword
        case Token.Type.KeywordFunction:
            return "fn"
        case Token.Type.KeywordIf:
            return "if"
        case Token.Type.KeywordElse:
            return "else"
        case Token.Type.KeywordDo:
            return "do"
        case Token.Type.KeywordFor:
            return "for"
        case Token.Type.KeywordWhile:
            return "while"
        # -Keyword: Type
        case Token.Type.KeywordVoid:
            return "void"
        case Token.Type.KeywordBoolean:
            return "bool"
        case Token.Type.KeywordInt8:
            return "int8"
        case Token.Type.KeywordInt16:
            return "int16"
        case Token.Type.KeywordInt32:
            return "int32"
        case Token.Type.KeywordInt64:
            return "int64"
        case Token.Type.KeywordUInt8:
            return "uint8"
        case Token.Type.KeywordUInt16:
            return "uint16"
        case Token.Type.KeywordUInt32:
            return "uint32"
        case Token.Type.KeywordUInt64:
            return "uint64"
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
        # -Symbol: Comparison
        case Token.Type.SymbolEqEq:
            return "=="
        case Token.Type.SymbolBangEq:
            return "!="
        case Token.Type.SymbolLt:
            return '<'
        case Token.Type.SymbolGt:
            return '>'
        case Token.Type.SymbolLtEq:
            return "<="
        case Token.Type.SymbolGtEq:
            return ">="
        # -Symbol: Misc
        case Token.Type.SymbolLParen:
            return '('
        case Token.Type.SymbolRParen:
            return ')'
        case Token.Type.SymbolLBrace:
            return '}'
        case Token.Type.SymbolRBrace:
            return '{'
        case Token.Type.SymbolComma:
            return ','
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
        KeywordTrue = auto()
        KeywordFalse = auto()
        # -Keyword
        KeywordFunction = auto()
        KeywordIf = auto()
        KeywordElse = auto()
        KeywordDo = auto()
        KeywordFor = auto()
        KeywordWhile = auto()
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
        # -Symbol: Operator
        SymbolEq = auto()
        SymbolPlus = auto()
        SymbolMinus = auto()
        SymbolStar = auto()
        SymbolFSlash = auto()
        SymbolPercent = auto()
        # -Symbol: Comparison
        SymbolEqEq = auto()
        SymbolBangEq = auto()
        SymbolLt = auto()
        SymbolGt = auto()
        SymbolLtEq = auto()
        SymbolGtEq = auto()
        # -Symbtl: Misc
        SymbolLParen = auto()
        SymbolRParen = auto()
        SymbolLBrace = auto()
        SymbolRBrace = auto()
        SymbolComma = auto()
        SymbolColon = auto()
        SymbolSemicolon = auto()

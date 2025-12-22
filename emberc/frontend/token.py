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
        value: str | None = None
    ) -> None:
        self.location: Location = location
        self.type: Token.Type = _type
        self._value: str | None = value

    # -Dunder Methods
    def __str__(self) -> str:
        _str = f"[{self.location}]{self.type.name}"
        if self._value is not None:
            _str += f"({self.value})"
        return _str

    # -Properties
    @property
    def value(self) -> str:
        assert self._value is not None
        return self._value

    # -Sub-Classes
    class Type(IntEnum):
        # -Literal
        Identifier = auto()
        Integer = auto()
        BooleanTrue = auto()
        BooleanFalse = auto()
        # -Symbol: Operator
        SymbolPlus = auto()
        SymbolMinus = auto()
        SymbolStar = auto()
        SymbolFSlash = auto()
        SymbolPercent = auto()
        # -Symbol: Misc
        SymbolLParen = auto()
        SymbolRParen = auto()
        SymbolSemicolon = auto()

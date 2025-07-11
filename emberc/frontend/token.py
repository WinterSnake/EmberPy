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
        _str = f"{self.location} {self.type.name}"
        if self.value:
            _str += f" '{self.value}'"
        return _str

    # -Sub-Classes
    class Type(IntEnum):
        '''Token Value Type'''
        # -Literals
        Integer = auto()
        # -Symbols
        Plus = auto()
        Minus = auto()
        Star = auto()
        FSlash = auto()
        Percent = auto()
        LParen = auto()
        RParen = auto()
        Semicolon = auto()

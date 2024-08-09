#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Token               ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from pathlib import Path

## Constants
__all__: tuple[str] = ("Token",)


## Classes
class Token:
    """
    Ember Language Token
    """

    # -Constructor
    def __init__(
        self, file: Path, position: tuple[int, int, int],
        _type: Token.Type, value: str | None = None
    ) -> None:
        self.file: Path = file
        self.position: tuple[int, int, int] = position
        self.type: Token.Type = _type
        self.value: str | None = value

    # -Dunder Methods
    def __repr__(self) -> str:
        return f"Token(file=\"{self.file}\", position={self.position}, type={self.type.name}, value='{self.value}')"

    def __str__(self) -> str:
        _str = f"{self.type.name}"
        if self.value:
            _str += f"<{self.value}>"
        return _str

    # -Properties
    @property
    def column(self) -> int:
        return self.position[1]

    @property
    def offset(self) -> int:
        return self.position[2]

    @property
    def row(self) -> int:
        return self.position[0]

    # -Sub-Classes
    class Type(IntEnum):
        # -Literals
        Identifier = auto()
        Integer = auto()
        # -Keywords
        KEYWORD_START = auto()
        KEYWORD_END = auto()
        # -Symbols: Single
        SINGLE_SYMBOL_START = auto()
        LParen = auto()     # (
        RParen = auto()     # )
        Semicolon = auto()  # ;
        Plus = auto()       # +
        Minus = auto()      # -
        Asterisk = auto()   # *
        FSlash = auto()     # /
        Percent = auto()    # %
        Equal = auto()      # =
        Greater = auto()    # >
        Less = auto()       # <
        SINGLE_SYMBOL_END = auto()
        # -Symbols: Multi


## Body
KEYWORD_COUNT: int = Token.Type.KEYWORD_END - Token.Type.KEYWORD_START - 1
SINGLE_SYMBOL_COUNT: int = Token.Type.SINGLE_SYMBOL_END - Token.Type.SINGLE_SYMBOL_START - 1

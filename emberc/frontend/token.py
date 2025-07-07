#!/usr/bin/python
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


## Classes
class Token:
    '''
    Ember Token
    Lexeme
    '''

    # -Constructor
    def __init__(
        self, file: Path, position: tuple[int, int, int],
        _type: Token.Type, value: int | str | None
    ) -> None:
        self.file: Path = file
        self.position: tuple[int, int, int] = position
        self.type: Token.Type = _type
        self.value: int | str | None = value

    # -Dunder Methods
    def __str__(self) -> str:
        _str = f"[{self.file}:{self.row}:{self.column}:{self.offset}]"
        _str += f"{self.type.name}"
        if self.value:
            _str += ' ' + f"'{self.value}'"
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
        '''
        Ember Token
        Value Type Enum
        '''

        # -Literals
        Identifier = auto()
        Integer = auto()
        # -Symbols
        LParen = auto()
        RParen = auto()
        Semicolon = auto()

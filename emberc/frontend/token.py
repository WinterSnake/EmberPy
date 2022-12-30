#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Token                         ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import Enum, auto
from pathlib import Path


## Classes
class Token:
    """"""

    # -Constructor
    def __init__(
        self, file: Path, position: tuple[int, int],
        _type: Token.Type, value: str | None = None
    ) -> None:
        self.file: Path = file
        self.position: tuple[int, int] = position
        self.type: Token.Type = _type
        self.value: str | None = value

    # -Dunder Methods
    def __repr__(self) -> str:
        return f"Token({self.file}, {self.position}, {self.type}, {self.value})"

    def __str__(self) -> str:
        return f"[{self.file}:{self.row}:{self.column}]{self.type.name}" + (
            f": \'{self.value}\'" if self.value else ""
        )

    # -Properties
    @property
    def column(self) -> int:
        return self.position[1]

    @property
    def row(self) -> int:
        return self.position[0]

    # -Sub-Classes
    class Type(Enum):
        ''''''
        IDENTIFIER = auto()
        # -Keywords
        # -Numbers
        NUMERIC = auto()
        # -Symbols
        LPAREN = auto()
        RPAREN = auto()
        SEMICOLON = auto()
        # -Symbols: Math
        ADD = auto()
        SUB = auto()
        MUL = auto()
        DIV = auto()
        MOD = auto()

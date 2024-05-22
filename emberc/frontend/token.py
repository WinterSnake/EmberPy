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
    """"""

    # -Constructor
    def __init__(
            self, file: Path, position: tuple[int, int, int],
            _type: Token.Type, value: str | None
    ) -> None:
        self.file: Path = file
        self.position: tuple[int, int, int] = position
        self.type: Token.Type = _type
        self.value: str | None = value

    # -Dunder Methods
    def __repr__(self) -> str:
        return f"Token(file={repr(self.file)}, position={self.position}, type={self.type}, value={self.value})"

    def __str__(self) -> str:
        return f"[{self.file}:{self.row}:{self.column}]{self.type.name}: '{self.value}'"

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

    # -Subclasses
    class Type(IntEnum):
        ''''''
        # -Symbols
        SymbolPlus = auto()
        SymbolMinus = auto()
        SymbolAsterisk = auto()
        SymbolSlash = auto()
        SymbolPercent = auto()
        SymbolLParen = auto()
        SymbolRParen = auto()
        SymbolSemicolon = auto()
        SymbolEqual = auto()
        # -Types
        TypeInt32 = auto()
        # -Literals
        Integer = auto()
        Identifier = auto()

#!/usr/bin/python
##-------------------------------##
## Ember: Frontend               ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Token Structure               ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from pathlib import Path


## Classes
class Token:
    """Ember Language Token"""

    # -Constructor
    def __init__(
        self, file_path: Path, position: tuple[int, int],
        type_: Token.TYPE, value: str | None = None
    ) -> None:
        self.file_path: Path = file_path
        self.position: tuple[int, int] = position
        self.type: Token.TYPE = type_
        self.value: str | None = value

    # -Dunder Methods
    def __repr__(self) -> str:
        str_: str = (
            f"Token(file_path={self.file_path}, "
            f"position={self.position}, type={repr(self.type)}"
        )
        if self.value is not None:
            str_ += f", value={self.value}"
        return str_ + ')'

    def __str__(self) -> str:
        str_: str = f"{self.type.name}"
        if self.value is not None:
            str_ += f":{self.value}"
        return str_

    # -Class Methods
    @classmethod
    def from_lexeme(
        cls, file_path: Path, position: tuple[int, int], value: str
    ) -> Token:
        '''Create Token from lexeme lookup'''
        type_, value_ = {
            # -KEYWORD
            # -COMPARISON
            "==": (Token.TYPE.EQUEQU, None),
            "!=": (Token.TYPE.NOTEQU, None),
            # -SYMBOL
            '+': (Token.TYPE.ADD, None),
            '-': (Token.TYPE.SUB, None),
            '*': (Token.TYPE.MUL, None),
            '/': (Token.TYPE.DIV, None),
            '%': (Token.TYPE.MOD, None),
            ';': (Token.TYPE.SEMICOLON, None),
            '(': (Token.TYPE.LPAREN, None),
            ')': (Token.TYPE.RPAREN, None),
        }.get(value, (None, value))
        if type_ is None:
            if value.isdigit():
                type_ = Token.TYPE.NUMBER
            else:
                type_ = Token.TYPE.IDENTIFIER
        return cls(file_path, position, type_, value_)

    # -Properties
    @property
    def row(self) -> int:
        return self.position[0]

    @property
    def column(self) -> int:
        return self.position[1]

    # -Sub-classes
    class TYPE(IntEnum):
        '''Token Type'''
        # -KEYWORD
        # -LITERAL
        IDENTIFIER = auto()
        NUMBER = auto()
        # -COMPARISON
        EQUEQU = auto()
        NOTEQU = auto()
        # -SYMBOL
        ADD = auto()
        SUB = auto()
        MUL = auto()
        DIV = auto()
        MOD = auto()
        SEMICOLON = auto()
        LPAREN = auto()
        RPAREN = auto()

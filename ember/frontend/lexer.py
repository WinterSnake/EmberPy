#!/usr/bin/python
##-------------------------------##
## Ember: Frontend               ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Lexer                         ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from pathlib import Path
from typing import TextIO

## Constants
SYMBOLS: tuple[str] = (
    # -MATH
    '+', '-', '*', '/', '%',
    # -COMPARISONS
    "==",
    # -OTHER
    '(', ')', '{', '}', ';',
)


## Functions
def lex_file(file_path: Path) -> list[Token]:
    """Parse file and return list of strings"""
    _lexer_check()
    lexemes: list[str] = []
    src: TextIO = file_path.open('r')
    row: int = 1
    col: int = 0
    tcol: int = 0
    buffer: str = ""
    while (char := src.read(1)):
        col += 1
        if char.isspace():
            if buffer:
                token = Token.from_lexeme(file_path, (row, tcol), buffer)
                lexemes.append(token)
                buffer = ""
            if char == '\n':
                row += 1
                col = 0
            continue
        elif char in SYMBOLS:
            if buffer:
                token = Token.from_lexeme(file_path, (row, tcol), buffer)
                lexemes.append(token)
                buffer = ""
            token = Token.from_lexeme(file_path, (row, col), char)
            lexemes.append(token)
            continue
        if not buffer:
            tcol = col
        buffer += char
    src.close()
    return lexemes


def _lexer_check():
    """Checks if all current token types are handled by the lexer"""
    unhandled_token_types: tuple[Token.TYPE] = tuple(
        type_
        for type_ in Token.TYPE
        if type_ not in (
            # -KEYWORD
            # -LITERAL
            Token.TYPE.IDENTIFIER,
            Token.TYPE.NUMBER,
            # -COMPARISON
            Token.TYPE.EQUEQU,
            # -SYMBOL
            Token.TYPE.ADD,
            Token.TYPE.SUB,
            Token.TYPE.MUL,
            Token.TYPE.DIV,
            Token.TYPE.MOD,
            Token.TYPE.SEMICOLON,
            Token.TYPE.LPAREN,
            Token.TYPE.RPAREN,
        )
    )
    if not unhandled_token_types:
        return None
    raise NotImplementedError(
        "Lexer unable to handle the following tokens: {}".format(
            ", ".join(f"'{type_.name}'" for type_ in unhandled_token_types)
        )
    )


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
        # -SYMBOL
        ADD = auto()
        SUB = auto()
        MUL = auto()
        DIV = auto()
        MOD = auto()
        SEMICOLON = auto()
        LPAREN = auto()
        RPAREN = auto()

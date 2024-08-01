#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Lexer               ##
##-------------------------------##

## Imports
from collections.abc import Generator
from pathlib import Path
from typing import TextIO

from .token import Token

## Constants
__all__: tuple[str] = ("Lexer",)
SYMBOLS: tuple[str, ...] = (
    "(", ")",
    # -Math
    "+", "-", "*", "/", "%",
)


## Classes
class Lexer:
    """
    """

    # -Constructor
    def __init__(self, file: Path) -> None:
        self.file: Path = file
        self._fp: TextIO | None = None
        self.row: int = 1
        self.column: int = 0
        self.offset: int = 0

    # -Dunder Methods
    def __repr__(self) -> str:
        return f"Lexer({self.file})"

    def __str__(self) -> str:
        return f"[{self.file}]"

    # -Instance Methods
    def _next(self) -> str | None:
        ''''''
        assert self._fp is not None
        if not self._fp.closed and (char := self._fp.read(1)):
            return char
        return None

    def _advance(self) -> str | None:
        ''''''
        char = self._next()
        self.offset += 1
        if char == '\n':
            self.row += 1
            self.column = 0
        elif char:
            self.column += 1
        return char

    def _peek(self) -> str | None:
        ''''''
        assert self._fp is not None
        position: int = self._fp.tell()
        char = self._next()
        if char:
            self._fp.seek(position)
        return char
    def lex(self) -> Generator[Token, None, None]:
        ''''''
        if self._fp is None:
            self._fp = self.file.open('r')
        while char := self._advance():
            # -[Word]
            if char.isalpha() or char == '_':
                yield self._lex_word(char)
            # -[Digit]
            elif char.isnumeric():
                yield self._lex_number(char)
            # -[Symbol]
            elif char in SYMBOLS:
                if (token := self._lex_symbol(char)) is not None:
                    yield token
        self._fp.close()

    def _lex_number(self, char: str) -> Token:
        ''''''
        value: str = char
        position: tuple[int, int, int] = self.position
        while char := self._peek():
            if char.isnumeric():
                value += self._advance()
            else:
                break
        return Token(self.file, position, Token.Type.Number, value)

    def _lex_symbol(self, char: str) -> Token:
        ''''''
        position: tuple[int, int, int] = self.position
        match char:
            case '+':
                return Token(self.file, position, Token.Type.Plus)
            case '-':
                return Token(self.file, position, Token.Type.Minus)
            case '*':
                return Token(self.file, position, Token.Type.Asterisk)
            case '/':
                return Token(self.file, position, Token.Type.FSlash)
            case '%':
                return Token(self.file, position, Token.Type.Percent)
        return None

    # -Properties
    @property
    def position(self) -> tuple[int, int, int]:
        return (self.row, self.column, self.offset)

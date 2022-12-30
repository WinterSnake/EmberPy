#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Lexer                         ##
##-------------------------------##

## Imports
from __future__ import annotations
from pathlib import Path
from typing import TextIO

from token import Token

## Constants
SYMBOLS = {
    '(': Token.Type.LPAREN,
    ')': Token.Type.RPAREN,
    ';': Token.Type.SEMICOLON,
    # -Math
    '+': Token.Type.ADD,
    '-': Token.Type.SUB,
    '*': Token.Type.MUL,
    '/': Token.Type.DIV,
    '%': Token.Type.MOD,
}


## Classes
class Lexer:
    """"""

    # -Constructor
    def __init__(self, file: Path) -> None:
        self.file: Path = file
        self.fp: TextIO = None  # type: ignore
        self.row: int = 1
        self.column: int = 0

    # -Instance Methods: Private
    def _advance(self) -> str | None:
        ''''''
        char = self._next()
        if char == '\n':
            self.row += 1
            self.column = 0
        else:
            self.column += 1
        return char

    def _next(self) -> str | None:
        ''''''
        if self.fp and not self.fp.closed:
            return self.fp.read(1)

    def _peek(self) -> str | None:
        ''''''
        position: int = self.fp.tell()
        char = self._next()
        if char:
            self.fp.seek(position)
        return char

    # -Instance Methods: Lexing
    def _lex(self) -> Token:
        ''''''
        while char := self._advance():
            # -Handle [WHITESPACE]
            if char.isspace():
                continue
            # -Handle [SYMBOL]
            elif char in SYMBOLS:
                return self._lex_symbol(char)
            # -Handle [NUMERIC]
            elif char.isdigit():
                return self._lex_numeric(char)
            # -Handle [IDENTIFIER]
            elif char.isalpha() or char == '_':
                return self._lex_identifier(char)
            # -Unknown
            else:
                print(f"Unknown character '{char}' in _lex")

    def _lex_symbol(self, char: str) -> Token:
        ''''''
        return Token(self.file, self.position, SYMBOLS[char])

    def _lex_numeric(self, char: str) -> Token:
        ''''''
        position: tuple[int, int] = self.position
        value = char
        while char := self._peek():
            if char.isspace():
                break
            elif char in SYMBOLS:
                break
            elif not char.isdigit():
                break
            else:
                value += char
                self._advance()
        return Token(self.file, position, Token.Type.NUMERIC, value)

    def _lex_identifier(self, char: str) -> Token:
        ''''''
        position: tuple[int, int] = self.position
        value = char
        while char := self._peek():
            if char.isspace():
                break
            elif char in SYMBOLS:
                break
            else:
                value += char
                self._advance()
        return Token(self.file, position, Token.Type.IDENTIFIER, value)

    # -Instance Methods: Public
    def get_next_token(self) -> Token:
        ''''''
        if not self.fp:
            self.fp = self.file.open('r')
        while token := self._lex():
            yield token
        self.fp.close()

    def get_tokens(self) -> list[Token, ...]:
        return list(token for token in self.get_next_token())

    # -Class Methods
    @classmethod
    def from_file_path(cls, file: str) -> Lexer:
        ''''''
        return cls(Path(file))

    # -Properties
    @property
    def position(self) -> tuple[int, int]:
        return (self.row, self.column)

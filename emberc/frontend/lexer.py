#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Lexer               ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Generator
from pathlib import Path
from typing import TextIO

from .token import Token

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
    """
    Ember Finite-State Lexer
    Each internal lexing method represents a state of the lexer
    Lookahead(1) operation
    """

    # -Constructor
    def __init__(self, file: Path, row: int = 1, column: int = 0) -> None:
        self.file: Path = file
        self.fp: TextIO = None  # type: ignore
        self.row: int = row
        self.column: int = column

    # -Instance Methods: Private
    def _advance(self) -> str | None:
        '''Get the next character from file and advance the lexer
        while incrementing file position'''
        char = self._next()
        if char == '\n':
            self.row += 1
            self.column = 0
        else:
            self.column += 1
        return char

    def _next(self) -> str | None:
        '''Read the next character from file'''
        if self.fp and not self.fp.closed:
            return self.fp.read(1)
        return None

    def _peek(self) -> str | None:
        '''Get the next character from file without advancing the lexer'''
        position: int = self.fp.tell()
        char = self._next()
        if char:
            self.fp.seek(position)
        return char

    # -Instance Methods: Lexing
    def _lex(self) -> Token | None:
        '''Internal lexing entry. Handles passing the lexer state to internal methods
        based on current character and start of lexeme'''
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
        return None

    def _lex_symbol(self, char: str) -> Token:
        '''LEX: Create symbol token from current character'''
        return Token(self.file, self.position, SYMBOLS[char])

    def _lex_numeric(self, char: str) -> Token:
        '''LEX: Create literal numeric by reading from current character
        until end of current lexeme'''
        position: tuple[int, int] = self.position
        value: str = char
        while _char := self._peek():
            if not _char:
                break
            elif _char.isspace():
                break
            elif _char in SYMBOLS:
                break
            elif not _char.isdigit():
                break
            else:
                value += _char
                self._advance()
        return Token(self.file, position, Token.Type.NUMERIC, value)

    def _lex_identifier(self, char: str) -> Token:
        '''LEX: Create literal identifier by reading from current character
        until end of current lexeme'''
        position: tuple[int, int] = self.position
        value: str = char
        while _char := self._peek():
            if not _char:
                break
            elif _char.isspace():
                break
            elif _char in SYMBOLS:
                break
            else:
                value += _char
                self._advance()
        return Token(self.file, position, Token.Type.IDENTIFIER, value)

    # -Class Methods
    @classmethod
    def from_file_path(cls, file: str, row: int = 1, column: int = 0) -> Lexer:
        '''Create lexer from file path and convert it into a Path object'''
        return cls(Path(file), row, column)

    # -Properties
    @property
    def closed(self) -> bool:
        if self.fp is None:
            return False
        return self.fp.closed

    @property
    def position(self) -> tuple[int, int]:
        return (self.row, self.column)

    @property
    def token_generator(self) -> Generator[Token, None, None]:
        '''Returns the lexer's token generator function'''
        if not self.fp:
            self.fp = self.file.open('r')
        while token := self._lex():
            yield token
        self.fp.close()
        return None

    @property
    def tokens(self) -> list[Token]:
        '''Returns a list of the lexer's tokens built from the token generator'''
        return list(token for token in self.token_generator)

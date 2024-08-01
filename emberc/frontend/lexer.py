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
    '(', ')', ';',
    # -Math
    '+', '-', '*', '/', '%',
)
KEYWORDS: tuple[str, ...] = (

)


## Classes
class Lexer:
    """
    Ember Language Finite State Lexer
    Lookahead(1) Operation
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
        '''Return next character from file or return None if at EOF or file is closed'''
        assert self._fp is not None
        if not self._fp.closed and (char := self._fp.read(1)):
            return char
        return None

    def _advance(self) -> str | None:
        '''Return next character from file and increment lexer position'''
        char = self._next()
        self.offset += 1
        if char == '\n':
            self.row += 1
            self.column = 0
        elif char:
            self.column += 1
        return char

    def _peek(self) -> str | None:
        '''Return next character without consuming from file'''
        assert self._fp is not None
        position: int = self._fp.tell()
        char = self._next()
        if char:
            self._fp.seek(position)
        return char

    def lex(self) -> Generator[Token, None, None]:
        '''Generate next token from lexer and close file when done'''
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

    def _lex_word(self, char: str) -> Token:
        '''Lex keyword or identifier and return token'''
        value: str = char
        position: tuple[int, int, int] = self.position
        while nchar := self._peek():
            if nchar.isalnum() or nchar == '_':
                nchar = self._advance()
                assert nchar is not None
                value += nchar
            else:
                break
        return Token(self.file, position, Token.Type.Identifier, value)

    def _lex_number(self, char: str) -> Token:
        '''Lex numeric value and return token'''
        value: str = char
        position: tuple[int, int, int] = self.position
        while nchar := self._peek():
            if nchar.isnumeric():
                nchar = self._advance()
                assert nchar is not None
                value += nchar
            else:
                break
        return Token(self.file, position, Token.Type.Number, value)

    def _lex_symbol(self, char: str) -> Token | None:
        '''Lex symbol and return token or none if in comment state'''
        match char:
            case '+':
                return Token(self.file, self.position, Token.Type.Plus)
            case '-':
                return Token(self.file, self.position, Token.Type.Minus)
            case '*':
                return Token(self.file, self.position, Token.Type.Asterisk)
            case '/':
                return self._lex_symbol_fslash()
            case '%':
                return Token(self.file, self.position, Token.Type.Percent)
            case ';':
                return Token(self.file, self.position, Token.Type.Semicolon)
            case _:
                return None

    def _lex_symbol_fslash(self) -> Token | None:
        '''Lex / symbol'''
        char = self._peek()
        match char:
            case '/':
                self._lex_comment_inline()
                return None
            case '*':
                self._lex_comment_multiline()
                return None
            case _:
                return Token(self.file, self.position, Token.Type.FSlash)

    def _lex_comment_inline(self) -> None:
        '''Lex inline comment until newline terminator found'''
        self._advance()  # -Consume comment start
        while char := self._advance():
            if char == '\n':
                return

    def _lex_comment_multiline(self) -> None:
        '''Lex multi-line comment until end terminator found'''
        self._advance()  # -Consume comment start
        while char := self._advance():
            if char == '*' and self._advance() == '/':
                return

    # -Properties
    @property
    def position(self) -> tuple[int, int, int]:
        return (self.row, self.column, self.offset)

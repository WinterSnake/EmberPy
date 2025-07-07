#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Lexer                         ##
##-------------------------------##

## Imports
from collections.abc import Generator
from pathlib import Path
from typing import TextIO
from .token import Token

## Constants
SYMBOLS: tuple[str, ...] = (
    '(', ')', ';',
)
KEYWORDS: dict[str, Token.Type] = {}


## Classes
class Lexer:
    """
    Ember Lexer
    Lookahead(1)
    """

    # -Constructor
    def __init__(self, file: Path) -> None:
        self.file: Path = file
        self.row: int = 1
        self.column: int = 0
        self.offset: int = 0
        # -IO
        self._fd: TextIO
        self._lookahead: str | None = None

    # -Instance Methods: Control
    def _advance(self) -> str | None:
        '''Retrieves next character and increments position'''
        current = self._next()
        if current == '\n':
            self.row += 1
            self.column = 0
        else:
            self.column += 1
        self.offset += 1
        return current

    def _peek(self) -> str | None:
        '''Retrieves next character and sets inner buffer'''
        current = self._next()
        self._lookahead = current
        return current

    def _next(self) -> str | None:
        '''Returns character from file or inner buffer'''
        if self._lookahead:
            value = self._lookahead
            self._lookahead = None
            return value
        return self._fd.read(1)

    # -Instance Methods: Lexing
    def lex(self) -> Generator[Token, None, None]:
        '''
        Open current lexer file and iterates over
        generated tokens from source.
        '''
        self._fd = self.file.open('r')
        while c := self._advance():
            token: Token | None = None
            # -Default -> Symbol
            if c in SYMBOLS:
                token = self._lex_symbol(c)
            # -Default -> Word
            elif c.isalpha() or c == '_':
                token = self._lex_word(c)
            # -Default -> Number
            elif c.isnumeric():
                token = self._lex_number(c)
            if token:
                yield token
        self._fd.close()

    def _lex_symbol(self, buffer: str) -> Token:
        '''
        Lexer State: Symbol
        Generates a symbol token
        '''
        symbol: Token.Type
        t_pos = self.position
        match buffer:
            case '(':
                symbol = Token.Type.LParen
            case ')':
                symbol = Token.Type.RParen
            case ';':
                symbol = Token.Type.Semicolon
        return Token(self.file, t_pos, symbol, None)

    def _lex_word(self, buffer: str) -> Token:
        '''
        Lexer State: Word
        Generates a keyword or identifier token
        '''
        t_pos = self.position
        while c := self._peek():
            # Word -> Word
            if c.isalnum() or c == '_':
                c = self._advance()
                assert(c)
                buffer += c
                continue
            # Word -> Default
            break
        _type = KEYWORDS.get(buffer, Token.Type.Identifier)
        return Token(
            self.file, t_pos, _type,
            buffer if _type == Token.Type.Identifier else None
        )

    def _lex_number(self, buffer: str) -> Token:
        '''
        Lexer State: Number
        Generates an integer token
        '''
        t_pos = self.position
        while c := self._peek():
            # Number -> Number
            if c.isnumeric():
                c = self._advance()
                assert(c)
                buffer += c
                continue
            # Number -> Default
            break
        return Token(
            self.file, t_pos, Token.Type.Integer,
            int(buffer)
        )

    # -Properties
    @property
    def position(self) -> tuple[int, int, int]:
        return (self.row, self.column, self.offset)

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
from ..location import Location

## Constants
SYMBOLS: dict[str, Token.Type] = {
    # -Operator
    '+': Token.Type.Plus,
    '-': Token.Type.Minus,
    '*': Token.Type.Star,
    '/': Token.Type.FSlash,
    '%': Token.Type.Percent,
    '=': Token.Type.Eq,
    # -Misc
    '(': Token.Type.LParen,
    ')': Token.Type.RParen,
    '{': Token.Type.LBrace,
    '}': Token.Type.RBrace,
    ';': Token.Type.Semicolon,
}
KEYWORDS: dict[str, Token.Type] = {
    'if': Token.Type.If,
    # -Types
    'int8': Token.Type.Int8,
    'int16': Token.Type.Int16,
    'int32': Token.Type.Int32,
    'int64': Token.Type.Int64,
    'uint8': Token.Type.UInt8,
    'uint16': Token.Type.UInt16,
    'uint32': Token.Type.UInt32,
    'uint64': Token.Type.UInt64,
}


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
    def _next(self) -> str | None:
        '''Returns character from file or inner buffer'''
        if self._lookahead:
            value = self._lookahead
            self._lookahead = None
            return value
        return self._fd.read(1)

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
            # -Default -> Number
            elif c.isnumeric():
                token = self._lex_number(c)
            # -Default -> Word
            elif c.isalpha() or c == '_':
                token = self._lex_word(c)
            # -Default -> Default
            elif c.isspace():
                continue
            # -Default -> Unknown
            else:
                print(f"Unexpected char '{c}'")
                return
            if token:
                yield token
        self._fd.close()

    def _lex_symbol(self, buffer: str) -> Token:
        '''
        Lexer State: Symbol
        Generates a symbol token
        '''
        symbol: Token.Type
        location = self.location
        symbol = SYMBOLS[buffer]
        return Token(location, symbol, None)

    def _lex_number(self, buffer: str) -> Token:
        '''
        Lexer State: Number
        Generates an integer token
        '''
        location = self.location
        while c := self._peek():
            # Number -> Number
            if c.isnumeric():
                c = self._advance()
                assert(c)
                buffer += c
                continue
            # Number -> Default
            break
        return Token(location, Token.Type.Integer, buffer)

    def _lex_word(self, buffer: str) -> Token:
        '''
        Lexer State: Word
        Generates a identifier or keyword token
        '''
        location = self.location
        while c := self._peek():
            # -Word -> Word
            if c.isalnum() or c == '_':
                c = self._advance()
                assert(c)
                buffer += c
                continue
            # -Word -> Default
            break
        _type = KEYWORDS.get(buffer, Token.Type.Identifier)
        value: str | None = buffer if _type == Token.Type.Identifier else None
        return Token(location, _type, value)

    # -Properties
    @property
    def position(self) -> tuple[int, int, int]:
        return (self.row, self.column, self.offset)

    @property
    def location(self) -> Location:
        return Location(self.file, self.position)

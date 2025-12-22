##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Lexer               ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Iterator
from pathlib import Path
from .lookahead_buffer import LookaheadBuffer
from .token import Token
from ..location import Location

## Constants
SYMBOLS = (
    '+', '-', '*', '/', '%',
    '(', ')', ';',
)
KEYWORDS = {
    'true': Token.Type.BooleanTrue,
    'false': Token.Type.BooleanFalse
}


## Classes
class Lexer(LookaheadBuffer[str, str]):
    """
    Ember Language Lexer
    Lookahead(1)

    Iterates over source file and yields a token where
    each lexer state is represented as an internal method.
    """

    # -Constructor
    def __init__(self, source: Iterator[str], file: Path | None = None):
        super().__init__(source)
        self.row: int = 1
        self.column: int = 0
        self.offset: int = 0
        self.file: Path | None = file

    # -Instance Methods
    # --Lookahead
    def advance(self) -> str | None:
        value = super().advance()
        if value == '\n':
            self.row += 1
            self.column = 0
        elif value is not None:
            self.column += 1
        if value is not None:
            self.offset += 1
        return value

    # --Lexing
    def lex(self) -> Iterator[Token]:
        '''Returns an iterator of tokens from source iterator'''
        while c := self.advance():
            token: Token | None = None
            # Default -> Symbol
            if c in SYMBOLS:
                token = self._lex_symbol(c)
            # Default -> Number
            elif c.isnumeric():
                token = self._lex_number(c)
            # Default -> Word
            elif c.isalpha() or c == '_':
                token = self._lex_word(c)
            if token:
                yield token

    def _lex_symbol(self, buffer: str) -> Token | None:
        '''
        Lexer State: Symbol

        Returns a symbol token or handles inline and multi-line consumption
        '''
        _type: Token.Type
        location = self.location
        match buffer:
            # -Operators
            case '+':
                _type = Token.Type.SymbolPlus
            case '-':
                _type = Token.Type.SymbolMinus
            case '*':
                _type = Token.Type.SymbolStar
            case '/':
                _type = Token.Type.SymbolFSlash
                if self.consume('/'):
                    self._lex_comment_inline()
                    return None
                elif self.consume('*'):
                    self._lex_comment_multiline()
                    return None
            case '%':
                _type = Token.Type.SymbolPercent
            # -Misc
            case '(':
                _type = Token.Type.SymbolLParen
            case ')':
                _type = Token.Type.SymbolRParen
            case ';':
                _type = Token.Type.SymbolSemicolon
        return Token(location, _type)

    def _lex_comment_inline(self) -> None:
        '''
        Lexer State: Comment - Inline
        Consumes characters until new line is reached
        '''
        c = self.advance()
        while c is not None and c != '\n':
            c = self.advance()

    def _lex_comment_multiline(self) -> None:
        '''
        Lexer State: Comment - Multiline
        Consumes characters until a multiline comment terminator
        is reached. Supports nested multiline comments.
        '''
        while c := self.advance():
            if c == '/' and self.advance() == '*':
                self._lex_comment_multiline()
            elif c == '*' and self.advance() == '/':
                return

    def _lex_number(self, buffer: str) -> Token:
        '''Lexer State: Number'''
        location = self.location
        while c := self.peek():
            # -Number -> Number
            if c.isnumeric():
                c = self.advance()
                assert c is not None
                buffer += c
                continue
            # -Number -> Default
            break
        return Token(location, Token.Type.Integer, buffer)

    def _lex_word(self, buffer: str) -> Token:
        '''Lexer State: Word'''
        location = self.location
        while c := self.peek():
            # -Word -> Word
            if c.isalnum() or c == '_':
                c = self.advance()
                assert c is not None
                buffer += c
                continue
            # -Word -> Default
            break
        _type = KEYWORDS.get(buffer, Token.Type.Identifier)
        value = buffer if _type == Token.Type.Identifier else None
        return Token(location, _type, value)

    # -Static Methods
    @staticmethod
    def from_file(file: Path) -> Lexer:
        '''Create a lexer from a given file'''
        def char_generator() -> Iterator[str]:
            with file.open('r') as f:
                while True:
                    char = f.read(1)
                    if not char:
                        break
                    yield char
        return Lexer(char_generator(), file)

    # -Properties
    @property
    def position(self) -> tuple[int, int, int]:
        return (self.row, self.column, self.offset)

    @property
    def location(self) -> Location:
        return Location(self.file, self.position)

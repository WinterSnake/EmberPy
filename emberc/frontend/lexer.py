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
from typing import TYPE_CHECKING
from .lookahead_buffer import LookaheadBuffer
from .token import Token
from ..location import Location

if TYPE_CHECKING:
    from ..ast import LITERAL_VALUE

## Constants
SYMBOLS = (
    # -Symbol: Math
    '=', '!',
    '+', '-', '*', '/', '%',
    # -Symbol: Bitwise
    '~', '^', '&', '|',
    # -Symbol: Comparison
    '<', '>',
    # -Symbol: Misc
    '.', ',', ':', ';', '@',
    '(', ')', '[', ']', '{', '}',
)
KEYWORDS = {
    # -Literals
    'true': Token.Type.Boolean,
    'false': Token.Type.Boolean,
    # -Keywords
    'if': Token.Type.KeywordIf,
    'else': Token.Type.KeywordElse,
    'while': Token.Type.KeywordWhile,
    'do': Token.Type.KeywordDo,
    'for': Token.Type.KeywordFor,
    'fn': Token.Type.KeywordFn,
    'return': Token.Type.KeywordReturn,
    # -Types
    'void': Token.Type.KeywordVoid,
    'bool': Token.Type.KeywordBoolean,
    'int8': Token.Type.KeywordInt8,
    'int16': Token.Type.KeywordInt16,
    'int32': Token.Type.KeywordInt32,
    'int64': Token.Type.KeywordInt64,
    'uint8': Token.Type.KeywordUInt8,
    'uint16': Token.Type.KeywordUInt16,
    'uint32': Token.Type.KeywordUInt32,
    'uint64': Token.Type.KeywordUInt64,
}


## Classes
class Lexer(LookaheadBuffer[str, str]):
    """
    Ember Lexer: Lookahead(1)

    Handles iterating over a string and churns out Ember related tokens.
    Can be used with either an iter(str) or a Pathlib file
    """

    # -Constructor
    def __init__(self, source: Iterator[str], file: Path | None = None):
        super().__init__(source)
        self.row: int = 1
        self.column: int = 0
        self.offset: int = 0
        self.file: Path | None = file

    # -Instance Methods: Lookahead
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

    # -Instance Methods: Lexing
    def lex(self) -> Iterator[Token]:
        '''
        State: Default
        '''
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
        State: Symbol
        '''
        _type: Token.Type
        location = self.location
        peeked = self.peek()
        match buffer:
            # -Symbol: Math
            case '=':
                _type = Token.Type.SymbolEq
                if self.consume('='):
                    _type = Token.Type.SymbolEqEq
            case '!':
                _type = Token.Type.SymbolBang
                if self.consume('='):
                    _type = Token.Type.SymbolNtEq
            case '+':
                _type = Token.Type.SymbolPlus
                if self.consume('='):
                    _type = Token.Type.SymbolPlusEq
            case '-':
                _type = Token.Type.SymbolMinus
                if self.consume('='):
                    _type = Token.Type.SymbolMinusEq
            case '*':
                _type = Token.Type.SymbolStar
                if self.consume('='):
                    _type = Token.Type.SymbolStarEq
            case '/':
                _type = Token.Type.SymbolFSlash
                if self.consume('/'):
                    self._lex_comment_inline()
                    return None
                elif self.consume('*'):
                    self._lex_comment_multiline()
                    return None
                elif self.consume('='):
                    _type = Token.Type.SymbolFSlashEq
            case '%':
                _type = Token.Type.SymbolPercent
                if self.consume('='):
                    _type = Token.Type.SymbolPercentEq
            # -Symbol: Bitwise
            case '~':
                _type = Token.Type.SymbolBitNeg
                if self.consume('='):
                    _type = Token.Type.SymbolBitNegEq
            case '^':
                _type = Token.Type.SymbolBitXor
                if self.consume('='):
                    _type = Token.Type.SymbolBitXorEq
            case '&':
                _type = Token.Type.SymbolBitAnd
                if self.consume('&'):
                    _type = Token.Type.SymbolLogAnd
                elif self.consume('='):
                    _type = Token.Type.SymbolBitAndEq
            case '|':
                _type = Token.Type.SymbolBitOr
                if self.consume('|'):
                    _type = Token.Type.SymbolLogOr
                elif self.consume('='):
                    _type = Token.Type.SymbolBitOrEq
            # -Symbol: Comparison
            case '<':
                _type = Token.Type.SymbolLt
                if self.consume('='):
                    _type = Token.Type.SymbolLtEq
                elif self.consume('<'):
                    _type = Token.Type.SymbolLShift
                    if self.consume('='):
                        _type = Token.Type.SymbolLShiftEq
            case '>':
                _type = Token.Type.SymbolGt
                if self.consume('='):
                    _type = Token.Type.SymbolGtEq
                elif self.consume('>'):
                    _type = Token.Type.SymbolRShift
                    if self.consume('='):
                        _type = Token.Type.SymbolRShiftEq
            # -Symbol: Misc
            case '.':
                _type = Token.Type.SymbolDot
                if self.consume('.'):
                    _type = Token.Type.SymbolDotDot
            case ',':
                _type = Token.Type.SymbolComma
            case ':':
                _type = Token.Type.SymbolColon
            case ';':
                _type = Token.Type.SymbolSemicolon
            case '@':
                _type = Token.Type.SymbolAt
            case '(':
                _type = Token.Type.SymbolLParen
            case ')':
                _type = Token.Type.SymbolRParen
            case '[':
                _type = Token.Type.SymbolLBracket
            case ']':
                _type = Token.Type.SymbolRBracket
            case '{':
                _type = Token.Type.SymbolLBrace
            case '}':
                _type = Token.Type.SymbolRBrace
            case _:
                raise NotImplementedError(f"'{buffer}' not handled in _lex_symbols()")
        return Token(location, _type)

    def _lex_comment_inline(self) -> None:
        '''
        State: Comment - Inline
        '''
        c = self.advance()
        while c is not None and c != '\n':
            c = self.advance()

    def _lex_comment_multiline(self) -> None:
        '''
        State: Comment - Multiline
        '''
        while c := self.advance():
            if c == '/' and self.advance() == '*':
                self._lex_comment_multiline()
            elif c == '*' and self.advance() == '/':
                return

    def _lex_number(self, buffer: str) -> Token:
        '''
        State: Number
        '''
        base: int = 10
        location = self.location
        while c := self.peek():
            # -Number -> Number
            if c.isnumeric():
                c = self.next()
                buffer += c
                continue
            # -Number -> Default
            break
        value = int(buffer, base)
        return Token(location, Token.Type.Integer, value)

    def _lex_word(self, buffer: str) -> Token:
        '''
        State: Word
        '''
        location = self.location
        while c := self.peek():
            # -Word -> Word
            if c.isalnum() or c == '_':
                c = self.next()
                buffer += c
                continue
            # -Word -> Default
            break
        _type = KEYWORDS.get(buffer, Token.Type.Identifier)
        value: LITERAL_VALUE | None = None
        if _type == Token.Type.Boolean:
            value = buffer == "true"
        elif _type == Token.Type.Identifier:
            value = buffer
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

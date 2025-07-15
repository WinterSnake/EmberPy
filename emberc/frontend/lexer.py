##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Lexer                         ##
##-------------------------------##

## Imports
from pathlib import Path
from collections.abc import Iterator
from typing import Any, TextIO
from .lookahead_buffer import LookaheadBuffer
from .token import Token
from ..errors import EmberError
from ..location import Location

## Constants
SYMBOLS: tuple[str, ...] = (
    '!',
    '=', '+', '-', '*', '/', '%',
    '<', '>',
    '(', ')', '{', '}', ':', ';',
)
KEYWORDS: dict[str, Token.Type] = {
    # -Literals
    'true': Token.Type.KeywordTrue,
    'false': Token.Type.KeywordFalse,
    # -Keywords
    'fn': Token.Type.KeywordFunction,
    'if': Token.Type.KeywordIf,
    'else': Token.Type.KeywordElse,
    'do': Token.Type.KeywordDo,
    'while': Token.Type.KeywordWhile,
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
    Ember Language Lexer
    Lookahead(1)

    Iterates over source file and yields a token where
    each lexer state is represented as an internal method.
    """

    # -Constructor
    def __init__(self, source: Path) -> None:
        self.errors: list[EmberError] = []
        # -Lookahead
        self._fp: TextIO
        # -State
        self.source: Path = source
        self.row: int = 1
        self.column: int = 0
        self.offset: int = 0

    # -Instance Methods: Control
    def _next(self) -> str | None:
        value: str | None
        value = self._fp.read(1)
        value = value if value else None
        return value

    def _advance(self) -> str | None:
        c = super()._advance()
        if c == '\n':
            self.row += 1
            self.column = 0
        elif c is not None:
            self.column += 1
        if c is not None:
            self.offset += 1
        return c

    def _error(self, code: int, **kwargs: Any) -> None:
        err = EmberError(code, self.location, **kwargs)
        self.errors.append(err)

    # -Instance Methods: Lex
    def lex(self) -> Iterator[Token]:
        '''
        Returns an iterator of created tokens from source file

        Errors: Unexpected character
        '''
        self._fp = self.source.open('r')
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
                self._error(EmberError.unexpected_character, char=c)
            if token:
                yield token
                token = None
        self._fp.close()

    def _lex_symbol(self, buffer: str) -> Token | None:
        '''
        Lexer State: Symbol
        Returns a symbol token or handles comment consumption

        Errors: Unknown symbol
        '''
        _type: Token.Type
        location = self.location
        match buffer:
            # -Operators
            case '=':
                _type = Token.Type.SymbolEq
                if self._consume('='):
                    _type = Token.Type.SymbolEqEq
            case '!':
                if self._consume('='):
                    _type = Token.Type.SymbolBangEq
                else:
                    self._error(EmberError.unknown_symbol, char=buffer)
                    return None
            case '+':
                _type = Token.Type.SymbolPlus
            case '-':
                _type = Token.Type.SymbolMinus
            case '*':
                _type = Token.Type.SymbolStar
            case '/':
                _type = Token.Type.SymbolFSlash
                if self._consume('/'):
                    self._lex_comment_inline()
                    return None
                elif self._consume('*'):
                    self._lex_comment_multiline()
                    return None
            case '%':
                _type = Token.Type.SymbolPercent
            # -Comparisons
            case '<':
                _type = Token.Type.SymbolLt
                if self._consume('='):
                    _type = Token.Type.SymbolLtEq
            case '>':
                _type = Token.Type.SymbolGt
                if self._consume('='):
                    _type = Token.Type.SymbolGtEq
            # -Misc
            case '(':
                _type = Token.Type.SymbolLParen
            case ')':
                _type = Token.Type.SymbolRParen
            case '{':
                _type = Token.Type.SymbolLBrace
            case '}':
                _type = Token.Type.SymbolRBrace
            case ':':
                _type = Token.Type.SymbolColon
            case ';':
                _type = Token.Type.SymbolSemicolon
            case _:
                self._error(EmberError.unknown_symbol, char=buffer)
                return None
        return Token(location, _type, None)

    def _lex_comment_inline(self) -> None:
        '''
        Lexer State: Comment - Inline
        Consumes characters until new line is reached
        '''
        c = self._advance()
        while c is not None and c != '\n':
            c = self._advance()


    def _lex_comment_multiline(self) -> None:
        '''
        Lexer State: Comment - Multiline
        Consumes characters until a multiline comment terminator
        is reached. Supports nested multiline comments.
        
        Errors: Unterminated comment multiline
        '''
        while c := self._advance():
            if c == '/' and self._consume('*'):
                self._lex_comment_multiline()
            elif c == '*' and self._consume('/'):
                return
        self._error(EmberError.unterminated_comment_multiline)


    def _lex_number(self, buffer: str) -> Token:
        '''
        Lexer State: Number
        Returns a number literal token
        '''
        location = self.location
        while c := self._peek():
            # Number -> Number
            if c.isnumeric():
                c = self._advance()
                assert c is not None
                buffer += c
                continue
            # Number -> Default
            break
        return Token(location, Token.Type.Integer, buffer)

    def _lex_word(self, buffer: str) -> Token:
        '''
        Lexer State: Word
        Returns a keyword token or an identifier tag token
        '''
        location = self.location
        while c := self._peek():
            # -Word -> Word
            if c.isalnum() or c == '_':
                c = self._advance()
                assert c is not None
                buffer += c
                continue
            # -Word -> Default
            break
        _type = KEYWORDS.get(buffer, Token.Type.Identifier)
        value = buffer if _type is Token.Type.Identifier else None
        return Token(location, _type, value)

    # -Properties
    @property
    def has_error(self) -> bool:
        return len(self.errors) > 0

    @property
    def position(self) -> tuple[int, int, int]:
        return (self.row, self.column, self.offset)

    @property
    def location(self) -> Location:
        return Location(self.source, self.position)

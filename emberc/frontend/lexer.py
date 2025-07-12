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
SYMBOLS: tuple[str, ...] = (
    '+', '-', '*', '/', '%',
    '=', '!', '<', '>',
    '(', ')', '{', '}', ',', ':', ';',
)
KEYWORDS: dict[str, Token.Type] = {
    'fn': Token.Type.KeywordFunction,
    'if': Token.Type.KeywordIf,
    'else': Token.Type.KeywordElse,
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
    # -Literals
    'true': Token.Type.LiteralTrue,
    'false': Token.Type.LiteralFalse,
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

    def _consume(self, char: str) -> bool:
        '''Consumes next character if expected char'''
        if self._peek() != char:
            return False
        _ = self._advance()
        return True

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
        match buffer:
            # -Operator
            case '+':
                symbol = Token.Type.SymbolPlus
            case '-':
                symbol = Token.Type.SymbolMinus
            case '*':
                symbol = Token.Type.SymbolStar
            case '/':
                symbol = Token.Type.SymbolFSlash
            case '%':
                symbol = Token.Type.SymbolPercent
            # -Comparison
            case '=':
                if self._consume('='):
                    symbol = Token.Type.SymbolEqEq
                else:
                    symbol = Token.Type.SymbolEq
            case '!':
                if self._consume('='):
                    symbol = Token.Type.SymbolBangEq
                else:
                    symbol = Token.Type.SymbolBang
            case '<':
                if self._consume('='):
                    symbol = Token.Type.SymbolLtEq
                else:
                    symbol = Token.Type.SymbolLt
            case '>':
                if self._consume('='):
                    symbol = Token.Type.SymbolGtEq
                else:
                    symbol = Token.Type.SymbolGt
            # -Misc
            case '(':
                symbol = Token.Type.SymbolLParen
            case ')':
                symbol = Token.Type.SymbolRParen
            case '{':
                symbol = Token.Type.SymbolLBrace
            case '}':
                symbol = Token.Type.SymbolRBrace
            case ',':
                symbol = Token.Type.SymbolComma
            case ':':
                symbol = Token.Type.SymbolColon
            case ';':
                symbol = Token.Type.SymbolSemicolon
            case _:
                print(f"Unknown symbol: '{buffer}'")
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

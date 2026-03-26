##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Lexer               ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import TYPE_CHECKING
from .token import Token
from ..core import Location, LookaheadBuffer

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path
    from typing import Self

## Constants
HEX_CHARACTERS = ('a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F')
SYMBOLS = (
    # -Math
    '+', '-', '*', '/', '%',
    # -Bitwise
    '~', '^', '&', '|',
    # -Comparison
    '=', '!', '<', '>',
    # -Misc
    '.', ',', ':', ';', '@',
    '(', ')', '[', ']', '{', '}',
)
KEYWORDS = {
    # -Literal
    'true': Token.Type.Boolean,
    'false': Token.Type.Boolean,
    # -Keyword
    'fn': Token.Type.KeywordFn,
    'struct': Token.Type.KeywordStruct,
    'union': Token.Type.KeywordUnion,
    'enum': Token.Type.KeywordEnum,
    'switch': Token.Type.KeywordSwitch,
    'case': Token.Type.KeywordCase,
    'if': Token.Type.KeywordIf,
    'else': Token.Type.KeywordElse,
    'while': Token.Type.KeywordWhile,
    'do': Token.Type.KeywordDo,
    'for': Token.Type.KeywordFor,
    'continue': Token.Type.KeywordContinue,
    'break': Token.Type.KeywordBreak,
    'return': Token.Type.KeywordReturn,
    'defer': Token.Type.KeywordDefer,
    'or': Token.Type.KeywordOr,
    'and': Token.Type.KeywordAnd,
    # -Type
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
    'ssize': Token.Type.KeywordSSize,
    'usize': Token.Type.KeywordUSize,
    # -Type: Modifier
    'const': Token.Type.KeywordConst,
    'immut': Token.Type.KeywordImmut,
}


## Functions
def _get_unescaped_sequence(char: str) -> str:
    """Returns the correct escape sequence string from a given char"""
    match char:
        case 'n':
            return '\n'
        case 'r':
            return '\r'
        case 't':
            return '\t'
        case '0':
            return '\0'
        case '\\':
            return '\\'
        case '\'':
            return '\''
        case '"':
            return '"'
    assert False, f"Unhandled escaped character '{char}'"


## Classes
class Lexer(LookaheadBuffer[str, str]):
    """
    Ember Lookahead(1) Lexer

    Transforms a raw character stream into a sequence of Ember tokens.
    Can be used with either a source string or file
    """

    # -Constructor
    def __init__(self, source: Iterator[str], file: Path | None = None):
        super().__init__(source)
        self.row: int = 1
        self.column: int = 0
        self.offset: int = -1
        self.file: Path | None = file

    # -Instance Methods: Lookahead
    def advance(self) -> str | None:
        if (value := super().advance()) is None:
            return None
        if value == '\n':
            self.row += 1
            self.column = 0
        else:
            self.column += 1
        self.offset += 1
        return value

    def requires(self, *expected: str) -> str:
        '''Returns next char if in expected chars; raises error otherwise'''
        if self.matches(*expected):
            return self.next()
        assert False, "TODO: Error handling"

    # -Instance Methods: Lexing
    def lex(self) -> Iterator[Token]:
        '''
        State: Default
        '''
        while c := self.advance():
            token: Token | None = None
            # Default -> Default
            if c.isspace():
                continue
            # Default -> Symbol
            elif c in SYMBOLS:
                token = self._lex_symbol(c)
            # Default -> Number
            elif c.isnumeric():
                token = self._lex_number(c)
            # Default -> Word
            elif c.isalpha() or c == '_':
                token = self._lex_word(c)
            # Default -> Char
            elif c == '\'':
                token = self._lex_char()
            # Default -> String
            elif c == '"':
                token = self._lex_string()
            if token:
                yield token

    def _lex_symbol(self, buffer: str) -> Token | None:
        '''
        State: Symbol
        '''
        _type: Token.Type
        location = self.location
        match buffer:
            # -Math
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
            # -Bitwise
            case '~':
                _type = Token.Type.SymbolBitNeg
            case '^':
                _type = Token.Type.SymbolBitXor
                if self.consume('='):
                    _type = Token.Type.SymbolBitXorEq
            case '&':
                _type = Token.Type.SymbolBitAnd
                if self.consume('='):
                    _type = Token.Type.SymbolBitAndEq
            case '|':
                _type = Token.Type.SymbolBitOr
                if self.consume('='):
                    _type = Token.Type.SymbolBitOrEq
            # -Comparison
            case '=':
                _type = Token.Type.SymbolEq
                if self.consume('='):
                    _type = Token.Type.SymbolEqEq
            case '!':
                _type = Token.Type.SymbolBang
                if self.consume('='):
                    _type = Token.Type.SymbolNtEq
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
            # -Misc
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
        while (c := self.advance()) and c != '\n':
            pass

    def _lex_comment_multiline(self) -> None:
        '''
        State: Comment - Multiline
        '''
        while c := self.advance():
            if c == '/' and self.consume('*'):
                self._lex_comment_multiline()
            elif c == '*' and self.consume('/'):
                return
        assert False, "[TODO]Syntax error: end of stream without multi-line comment termination"

    def _lex_number(self, buffer: str) -> Token:
        '''
        State: Number
        '''
        base = 10
        location = self.location
        if buffer == '0' and self.matches('b', 'o', 'x'):
            # -Binary
            if self.consume('b'):
                base = 2
            # -Octal
            elif self.consume('o'):
                base = 8
            # -Hex
            elif self.consume('x'):
                base = 16
            buffer = ''
        while c := self.peek():
            # -Number: Digit
            if c.isnumeric():
                buffer += self.next()
                continue
            # -Number: Hex
            elif c in HEX_CHARACTERS and base == 16:
                buffer += self.next()
                continue
            # Number -> Default
            break
        return Token(location, Token.Type.Integer, int(buffer, base))

    def _lex_word(self, buffer: str) -> Token:
        '''
        State: Word
        '''
        location = self.location
        while c := self.peek():
            # -Word: Alphanumber or '_'
            if c.isalnum() or c == '_':
                buffer += self.next()
                continue
            # World -> Default
            break
        _type = KEYWORDS.get(buffer, Token.Type.Identifier)
        value: bool | str | None = None
        if _type == Token.Type.Boolean:
            value = buffer == "true"
        elif _type == Token.Type.Identifier:
            value = buffer
        return Token(location, _type, value)

    def _lex_char(self) -> Token:
        '''
        State: Char
        '''
        location = self.location
        value = self.next()
        if value == '\\':
            value = _get_unescaped_sequence(self.next())
        _ = self.requires('\'')
        return Token(location, Token.Type.Integer, ord(value))

    def _lex_string(self) -> Token:
        '''
        State: String
        '''
        location = self.location
        buffer = ""
        while c := self.next():
            # String -> Default
            if c == '"':
                break
            # String -> Escaped
            elif c == '\\':
                c = _get_unescaped_sequence(self.next())
            buffer += c
        return Token(location, Token.Type.String, buffer)

    # -Class Methods
    @classmethod
    def from_file(cls, file: Path, chunk_size: int = 4096) -> Self:
        '''Create a Lexer instance from a given source file'''
        # -Internal Functions
        def _generate_chars() -> Iterator[str]:
            with file.open('r', encoding='utf-8') as f:
                while chunk := f.read(chunk_size):
                    yield from chunk
        # -Body
        return cls(_generate_chars(), file)

    @classmethod
    def from_str(cls, source: str) -> Self:
        '''Create a Lexer instance from a given source string'''
        return cls(iter(source))

    # -Properties
    @property
    def position(self) -> tuple[int, int, int]:
        return (self.row, self.column, self.offset)

    @property
    def location(self) -> Location:
        return Location(self.file, self.position)

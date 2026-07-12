##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Lexer               ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING, Self
from .token import Token
from ..core import LookaheadBuffer, Span

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path
    from ..diagnostics import DiagnosticEngine

## Constants
SYMBOLS = (
    # -Math
    '=',
    '+', '-', '*', '/', '%',
    # -Misc
    ',', ';', '(', ')',
)
KEYWORDS: dict[str, Token.Kind] = {
    # -Types
    'int32': Token.Kind.KeywordInt32,
}


## Classes
class Lexer(LookaheadBuffer[str, str]):
    """
    Ember Lookahead(1) Lexer

    A lookahead lexer for the Ember compiler that converts raw text into a stream of tokens.
    Tracks row, column, and global offsets during execution to attach precise `Span` 
    metadata to tokens and interfaces with a `DiagnosticEngine` to report lexical errors.
    """

    # -Constructor
    def __init__(
        self, _id: int, source: Iterator[str], engine: DiagnosticEngine
    ) -> None:
        super().__init__(source)
        # -Location
        self.id: int = _id
        self.row: int = 1
        self.column: int = 0
        self.offset: int = 0
        # -Diagnostics
        self._engine: DiagnosticEngine = engine

    # -Dunder Methods
    def __iter__(self) -> Self:
        return self

    def __next__(self) -> Token:
        while not self.is_at_end:
            token = self._lex()
            if token is not None:
                return token
        raise StopIteration

    # -Instance Methods: Lookahead
    def advance(self) -> str | None:
        if (char := super().advance()) is None:
            return None
        if char == '\n':
            self.row += 1
            self.column = 0
        else:
            self.column += 1
        self.offset += 1
        return char

    # -Instance Methods: Lexing
    def _lex(self) -> Token | None:
        '''
        State: Default
        '''
        while c := self.advance():
            # -Default -> Default
            if c.isspace():
                continue
            # -Default -> Symbol
            elif c in SYMBOLS:
                return self._lex_symbol(c)
            # -Default -> Number
            elif c.isnumeric():
                return self._lex_number(c)
            # -Default -> Word
            elif c.isalpha() or c == '_':
                return self._lex_word(c)
        # -TODO: report unknown character through diagnostic engine
        return None

    def _lex_symbol(self, buffer: str) -> Token | None:
        '''
        State: Symbol
        '''
        kind: Token.Kind
        start = self.byte_offset
        match buffer:
            # -Math
            case '=':
                kind = Token.Kind.SymbolEq
            case '+':
                kind = Token.Kind.SymbolPlus
            case '-':
                kind = Token.Kind.SymbolMinus
            case '*':
                kind = Token.Kind.SymbolStar
            case '/':
                kind = Token.Kind.SymbolFSlash
            case '%':
                kind = Token.Kind.SymbolPercent
            # -Misc
            case ',':
                kind = Token.Kind.SymbolComma
            case ';':
                kind = Token.Kind.SymbolSemicolon
            case '(':
                kind = Token.Kind.SymbolLParen
            case ')':
                kind = Token.Kind.SymbolRParen
            case _:
                raise NotImplementedError(f"Symbol '{buffer}' not handled in lexer")
        return Token(self._create_span(start), kind, None)

    def _lex_number(self, buffer: str) -> Token:
        '''
        State: Number
        '''
        base = 10
        start = self.byte_offset
        while c := self.peek():
            # Number -> Number
            if c.isnumeric():
                buffer += self.next()
                continue
            # Number -> Default
            break
        return Token(
            self._create_span(start),
            Token.Kind.Integer, int(buffer)
        )

    def _lex_word(self, buffer: str) -> Token:
        '''
        State: Word
        '''
        start = self.byte_offset
        while c := self.peek():
            # Word -> Word
            if c.isalnum() or c == '_':
                buffer += self.next()
                continue
            # Word -> Default
            break
        kind = KEYWORDS.get(buffer, Token.Kind.Identifier)
        value = buffer if kind is Token.Kind.Identifier else None
        return Token(self._create_span(start), kind, value)

    # -Instance Methods: Helpers
    def _create_span(self, start: int) -> Span:
        return Span(self.id, start, self.offset)

    # -Class Methods
    @classmethod
    def from_source_map(cls, _id: int, engine: DiagnosticEngine) -> Self:
        _iter = engine.source_map[_id].get_iter()
        return cls(_id, _iter, engine)

    # -Properties
    @property
    def byte_offset(self) -> int:
        return self.offset - 1

    # -Class Properties
    __slots__ = ('id', 'row', 'column', 'offset', '_engine')

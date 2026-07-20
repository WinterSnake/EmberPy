##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Lexer               ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING, Self
from .comment import Comment
from .token import Token
from ..core import LookaheadBuffer, Span

if TYPE_CHECKING:
    from collections.abc import Iterator, MutableSequence
    from ..diagnostics import DiagnosticEngine

## Constants
SYMBOLS = (
    # -Math
    '+', '-', '*', '/', '%',
    # -Assignment + Comparisons
    '=', '!', '<', '>',
    # -Misc
    ',', ';', '(', ')', '{', '}',
)
KEYWORDS = {
    # -Literals
    'true': Token.Kind.Boolean,
    'false': Token.Kind.Boolean,
    # -Keywords
    'if': Token.Kind.KeywordIf,
    'else': Token.Kind.KeywordElse,
    # -Keyword: Types
    'void': Token.Kind.KeywordVoid,
    'bool': Token.Kind.KeywordBoolean,
    'int8': Token.Kind.KeywordInt8,
    'int16': Token.Kind.KeywordInt16,
    'int32': Token.Kind.KeywordInt32,
    'int64': Token.Kind.KeywordInt64,
    'uint8': Token.Kind.KeywordUInt8,
    'uint16': Token.Kind.KeywordUInt16,
    'uint32': Token.Kind.KeywordUInt32,
    'uint64': Token.Kind.KeywordUInt64,
    'isize': Token.Kind.KeywordISize,
    'usize': Token.Kind.KeywordUSize,
}


## Classes
class Lexer(LookaheadBuffer[str, str]):
    """
    Ember Lexer [Lookahead(1)]

    Transform a character source stream into a stream of tokens.
    Track and store comments and line offsets within the source text,
    and handle diagnostic reporting through the engine.
    """
    # -Constructor
    def __init__(
        self, _id: int, source: Iterator[str], engine: DiagnosticEngine
    ) -> None:
        super().__init__(source, None)
        self.id = _id
        self.engine = engine
        self.offset = 0
        self._line_offsets: MutableSequence[int] = [0]
        self._comments: MutableSequence[Comment] = []

    # -Instance Methods: Lookahead
    def advance(self) -> str | None:
        '''Advance the stream by one and update source location; return item or None if at end.'''
        if (c := super().advance()) is None:
            return None
        self.offset += 1
        if c == '\n':
            self._line_offsets.append(self.offset)
        return c

    # -Instance Methods: Lexing
    def get_token_iter(self) -> Iterator[Token]:
        '''Return a token iterator from source stream until exhausted; updates source metadata on completion.'''
        while not self.is_at_end:
            token = self._lex()
            if token:
                yield token
        self.engine.source_map[self.id].comments = tuple(self._comments)
        self.engine.source_map[self.id].line_offsets = tuple(self._line_offsets)

    def _lex(self) -> Token | None:
        '''
        State: Default
        '''
        while c := self.advance():
            # Default -> Default
            if c.isspace():
                continue
            # Default -> Symbol
            elif c in SYMBOLS:
                return self._lex_symbol(c)
            # Default -> Number
            elif c.isnumeric():
                return self._lex_number()
            # Default -> Word
            elif c.isalpha() or c == '_':
                return self._lex_word()
            # [Unknown] TODO: Report error to engine
        return None

    def _lex_symbol(self, symbol: str) -> Token | None:
        '''
        State: Symbol
        '''
        kind: Token.Kind
        start = self.byte_offset
        match symbol:
            case '+':
                kind = Token.Kind.SymbolPlus
            case '-':
                kind = Token.Kind.SymbolMinus
            case '*':
                kind = Token.Kind.SymbolStar
            case '/':
                kind = Token.Kind.SymbolFSlash
                if self.consume('/'):
                    comment = self._lex_comment_inline(start)
                    self._comments.append(comment)
                    return None
                elif self.consume('*'):
                    comment = self._lex_comment_multi(start)
                    self._comments.append(comment)
                    return None
            case '%':
                kind = Token.Kind.SymbolPercent
            case '=':
                kind = Token.Kind.SymbolEq
                if self.consume('='):
                    kind = Token.Kind.SymbolEqEq
            case '!':
                kind = Token.Kind.SymbolBang
                if self.consume('='):
                    kind = Token.Kind.SymbolBangEq
            case '<':
                kind = Token.Kind.SymbolLt
                if self.consume('='):
                    kind = Token.Kind.SymbolLtEq
            case '>':
                kind = Token.Kind.SymbolGt
                if self.consume('='):
                    kind = Token.Kind.SymbolGtEq
            case ',':
                kind = Token.Kind.SymbolComma
            case ';':
                kind = Token.Kind.SymbolSemicolon
            case '(':
                kind = Token.Kind.SymbolLParen
            case ')':
                kind = Token.Kind.SymbolRParen
            case '{':
                kind = Token.Kind.SymbolLBrace
            case '}':
                kind = Token.Kind.SymbolRBrace
            case _:
                raise NotImplementedError(f"Symbol '{symbol}' not handled in symbol lexing.")
        return Token(self._span_from(start), kind, None)

    def _lex_comment_inline(self, start: int) -> Comment:
        '''
        State: Comment[Inline]
        '''
        while not self.consume('\n') and not self.is_at_end:
            _ = self.next()
        return Comment(self._span_from(start, self.byte_offset), None)

    def _lex_comment_multi(self, start: int) -> Comment:
        '''
        State: Comment[Multi]
        '''
        children: list[Comment] = []
        while c := self.advance():
            if c == '*' and self.consume('/'):
                break
            elif c == '/' and self.consume('*'):
                child = self._lex_comment_multi(self.offset - 2)
                children.append(child)
        return Comment(self._span_from(start), tuple(children))

    def _lex_number(self) -> Token:
        '''
        State: Number
        '''
        base = 10
        start = self.byte_offset
        while c := self.peek():
            # Number -> Number
            if c.isnumeric():
                _ = self.advance()
                continue
            # Number -> Default
            break
        span = self._span_from(start)
        buffer = self._buffer_from(span)
        value = int(buffer, base)
        return Token(span, Token.Kind.Integer, value)

    def _lex_word(self) -> Token:
        '''
        State: Word
        '''
        start = self.byte_offset
        while c := self.peek():
            # Word -> Word
            if c.isalnum() or c == '_':
                _ = self.advance()
                continue
            # Word -> Default
            break
        span = self._span_from(start)
        buffer = self._buffer_from(span)
        kind = KEYWORDS.get(buffer, Token.Kind.Identifier)
        value: bool | str | None
        if kind is Token.Kind.Boolean:
            value = buffer == "true"
        else:
            value = buffer if kind is Token.Kind.Identifier else None
        return Token(span, kind, value)

    # -Instance Methods: Helpers
    def _buffer_from(self, span: Span) -> str:
        return self.engine.source_map.get_text_span(span)

    def _span_from(self, start: int, end: int | None = None) -> Span:
        if end is None:
            end = self.offset
        return Span(self.id, start, end)

    # -Class Methods
    @classmethod
    def from_source_id(cls, _id: int, engine: DiagnosticEngine) -> Self:
        '''Create lexer from the given diagnostic engine with mapped id.'''
        _iter = engine.source_map[_id].get_text_iter()
        return cls(_id, _iter, engine)

    # -Properties
    @property
    def byte_offset(self) -> int:
        return self.offset - 1

    # -Class Properties
    __slots__ = (
        "id",
        "engine",
        "offset",
        "_comments",
        "_line_offsets",
    )

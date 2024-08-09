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
from typing import TextIO, cast

from .token import KEYWORD_COUNT, SINGLE_SYMBOL_COUNT, Token

## Constants
SYMBOLS: tuple[str, ...] = (
    # -Math
    '+', '-', '*', '/', '%',
    # -Assignment
    '=',
    # -Comparison
    '>', '<',
    # -Misc
    '(', ')', ':', ';',
)
KEYWORDS: dict[str, Token.Type] = {
    'if': Token.Type.KeywordIf,
    'else': Token.Type.KeywordElse,
    'for': Token.Type.KeywordFor,
    'while': Token.Type.KeywordWhile,
    'do': Token.Type.KeywordDo,
    'fn': Token.Type.KeywordFunction,
    'return': Token.Type.KeywordReturn,
}


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
        _str = f"Lexer(file=\"{self.file}\", "
        if self._fp and not self._fp.closed:
            _str += f"position={self.position}, status=OPEN"
        else:
            _str += "status=CLOSED"
        return _str + ')'

    # -Instance Methods
    def lex(self) -> Generator[Token, None, None]:
        '''Generate next token from file'''
        if not self._fp:
            self._fp = self.file.open('r')
        while char := self._advance():
            token: Token | None = None
            # -State[DEFAULT] > State[WORD]
            if char.isalpha() or char == '_':
                token = self._lex_word(char)
            # -State[DEFAULT] > State[DIGIT]
            elif char.isnumeric():
                token = self._lex_digit(char)
            # -State[DEFAULT] > State[SYMBOL]
            elif char in SYMBOLS:
                token = self._lex_symbol(char)
            else:
                continue
            # -Return token
            if token:
                yield token
        self._fp.close()

    # -Instance Methods: Read
    def _advance(self) -> str | None:
        '''Return next character and increment lexer position'''
        char = self._next()
        if char is None:
            return None
        if char == '\n':
            self.row += 1
            self.column = 0
        else:
            self.column += 1
        self.offset += 1
        return char

    def _match(self, expected: str) -> bool:
        '''Consumes next char and returns true if expected char matches peeked char'''
        actual = self._peek()
        if actual != expected:
            return False
        self._advance()
        return True

    def _next(self) -> str | None:
        '''Return next character from file or return None if EOF or file is closed'''
        assert self._fp is not None
        if not self._fp.closed:
            return self._fp.read(1)
        return None

    def _peek(self) -> str | None:
        '''Return next character without incrementing reader pointer'''
        assert self._fp is not None
        if self._fp.closed:
            return None
        position: int = self._fp.tell()
        char = self._next()
        if char:
            self._fp.seek(position)
        return char

    # -Instance Methods: State
    def _lex_comment_inline(self) -> None:
        '''Advance lexer to new line terminator'''
        while char := self._advance():
            if char == '\n':
                return

    def _lex_comment_multi(self) -> None:
        '''Advance lexer to multiline comment terminator'''
        # -TODO: Nested Multiline comment
        while char := self._advance():
            if char == '*' and self._advance() == '/':
                return

    def _lex_digit(self, buffer: str) -> Token:
        '''Return lexed numeric literal token'''
        # -TODO: Handle float
        # -TODO: Handle format: [binary, hex]
        position = self.position
        while char := self._peek():
            # -State[DIGIT] > State[DIGIT]
            if char.isnumeric():
                buffer += cast(str, self._advance())
            # -State[DIGIT] > STATE[DEFAULT]
            else:
                break
        return Token(self.file, position, Token.Type.Integer, buffer)

    def _lex_symbol(self, buffer: str) -> Token | None:
        '''Return lexed symbol token or None if inline/multi-line comment'''
        # -TODO: Handle assignment operators
        # -TODO: Handle comparison operators
        position: tuple[int, int, int] = self.position
        match buffer:
            # -Token[LParen]
            case '(':
                return Token(self.file, position, Token.Type.LParen)
            # -Token[RParen]
            case ')':
                return Token(self.file, position, Token.Type.RParen)
            # -Token[Colon]
            case ':':
                return Token(self.file, position, Token.Type.Colon)
            # -Token[Semicolon]
            case ';':
                return Token(self.file, position, Token.Type.Semicolon)
            case '=':
                # -Token[EQUALEQUAL]
                if self._match('='):
                    return Token(self.file, position, Token.Type.EqualEqual)
                # -Token[EQUAL]
                return Token(self.file, position, Token.Type.Equal)
            case '>':
                # -Token[GREATEREQUAL]
                if self._match('='):
                    return Token(self.file, position, Token.Type.GreaterEqual)
                # -Token[GREATER]
                return Token(self.file, position, Token.Type.Greater)
            case '<':
                # -Token[LESSEQUAL]
                if self._match('='):
                    return Token(self.file, position, Token.Type.LessEqual)
                # -Token[LESS]
                return Token(self.file, position, Token.Type.Less)
            case '+':
                # -Token[PLUSEQUAL]
                if self._match('='):
                    return Token(self.file, position, Token.Type.PlusEqual)
                # -Token[PLUSPLUS]
                elif self._match('+'):
                    return Token(self.file, position, Token.Type.PlusPlus)
                # -Token[PLUS]
                return Token(self.file, position, Token.Type.Plus)
            case '-':
                # -Token[MINUSEQUAL]
                if self._match('='):
                    return Token(self.file, position, Token.Type.MinusEqual)
                # -Token[MINUSMINUS]
                elif self._match('-'):
                    return Token(self.file, position, Token.Type.MinusMinus)
                # -Token[MINUS]
                return Token(self.file, position, Token.Type.Minus)
            case '*':
                # -Token[ASTERISKEQUAL]
                if self._match('='):
                    return Token(self.file, position, Token.Type.AsteriskEqual)
                # -Token[ASTERISK]
                return Token(self.file, position, Token.Type.Asterisk)
            case '/':
                # -State[SYMBOL] > State[COMMENT-INLINE]
                if self._match('/'):
                    self._lex_comment_inline()
                    return None
                # -State[SYMBOL] > State[COMMENT-MULTI]
                elif self._match('*'):
                    self._lex_comment_multi()
                    return None
                # -Token[FSLASHEQUAL]
                if self._match('='):
                    return Token(self.file, position, Token.Type.FSlashEqual)
                # -Token[FSLASH]
                return Token(self.file, position, Token.Type.FSlash)
            case '%':
                # -Token[PERCENTEQUAL]
                if self._match('='):
                    return Token(self.file, position, Token.Type.PercentEqual)
                # -Token[PERCENT]
                return Token(self.file, position, Token.Type.Percent)
        assert False, f"Unreachable: {buffer}"

    def _lex_word(self, buffer: str) -> Token:
        '''Return lexed word token with keyword checking'''
        position = self.position
        while char := self._peek():
            # -State[WORD] > State[WORD]
            if char.isalnum() or char == '_':
                buffer += cast(str, self._advance())
            # -State[WORD] > State[DEFAULT]
            else:
                break
        # -Keywords | Identifier
        # -TODO: Handle keywords
        _type: Token.Type = KEYWORDS.get(buffer, Token.Type.Identifier)
        return Token(
            self.file, position, _type,
            buffer if _type is Token.Type.Identifier else None
        )

    # -Properties
    @property
    def position(self) -> tuple[int, int, int]:
        return (self.row, self.column, self.offset)


## Body
assert len(SYMBOLS) == SINGLE_SYMBOL_COUNT
assert len(KEYWORDS) == KEYWORD_COUNT

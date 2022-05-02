#!/usr/bin/python
##-------------------------------##
## Ember: Frontend               ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Lexer                         ##
##-------------------------------##

## Imports
from __future__ import annotations
from pathlib import Path
from typing import TextIO

from .token import Token

## Constants
SYMBOLS: tuple[str, ...] = (
    # -MATH
    '+', '-', '*', '/', '%', '=',
    # -OTHER
    '!', '(', ')', '{', '}', ';',
)


## Classes
class Lexer:
    """Ember Finite State Machine Lexer
    Each method is a state during lexing a file
    Lookahead(1) operation"""

    # -Constructor
    def __init__(self, file_path: Path, line: int = 1, column: int = 0) -> None:
        self.file_path: Path = file_path
        self.fp: TextIO = None  #type: ignore
        self.line: int = line
        self.column: int = column

    # -Dunder Methods
    def __iter__(self) -> Lexer:
        return self

    def __next__(self) -> Token | None:
        if token := self.get_next_token():
            return token
        raise StopIteration()

    # -Instance Methods: Private
    def _next(self) -> str | None:
        '''Internal character reader'''
        if not self.fp.closed and (char := self.fp.read(1)):
            return char
        return None

    def _peek(self) -> str | None:
        '''Returns next character without advancing lexer position'''
        assert self.fp is not None
        position: int = self.fp.tell()
        char = self._next()
        if char:
            self.fp.seek(position)
        return char

    def _advance(self) -> str | None:
        '''Returns next character and advances lexer position'''
        assert self.fp is not None
        char = self._next()
        if char == '\n':
            self.line += 1
            self.column = 0
        elif char:
            self.column += 1
        return char

    def _lex(self) -> Token | None:
        '''Internal lexer generator'''
        while char := self._advance():
            # -[WHITESPACE]
            if char.isspace():
                continue
            # -[SYMBOL]
            elif char in SYMBOLS:
                return self._lex_symbol(char)
            # -[NUMBER]
            elif char.isdigit():
                return self._lex_number(char)
            # -[IDENTIFIER]
            elif char.isalpha() or char == '_':
                return self._lex_identifier(char)
            # -[ERROR]
            else:
                raise SyntaxError(f"Unhandled char '{char}' in lexer.lex")
        return None

    def _lex_identifier(self, char: str) -> Token:
        '''Internal IDENTIFIER lexer state'''
        nchar: str | None
        pos: tuple[int, int] = self.position
        buffer: str = char
        while nchar := self._peek():
            if nchar.isalpha() or nchar.isdigit() or nchar in ('_', ):
                buffer += nchar
                self._advance()
            elif nchar.isspace() or nchar in SYMBOLS:
                break
            else:
                raise SyntaxError(f"Unhandled char '{nchar}' in lexer.identifier")
        return Token(self.file_path, pos, Token.TYPE.IDENTIFIER, buffer)

    def _lex_number(self, char: str) -> Token:
        '''Internal NUMBER lexer state'''
        nchar: str | None
        pos: tuple[int, int] = self.position
        buffer: str = char
        while nchar := self._peek():
            if nchar.isdigit():
                buffer += nchar
                self._advance()
            elif nchar.isspace() or nchar in SYMBOLS:
                break
            else:
                raise SyntaxError(f"Unhandled char '{nchar}' in lexer.number")
        return Token(self.file_path, pos, Token.TYPE.NUMBER, buffer)

    def _lex_symbol(self, char: str) -> Token | None:
        '''Internal SYMBOL lexer state'''
        pos: tuple[int, int] = self.position
        type_: Token.TYPE | None = None
        # --Symbol: +
        if char == '+':
            type_ = Token.TYPE.ADD
        # --Symbol: -
        elif char == '-':
            type_ = Token.TYPE.SUB
        # --Symbol: *
        elif char == '*':
            type_ = Token.TYPE.MUL
        # --Symbol: /
        elif char == '/':
            type_ = Token.TYPE.DIV
        # --Symbol: %
        elif char == '%':
            type_ = Token.TYPE.MOD
        # --Symbol: = | ==
        elif char == '=':
            if self._peek() == '=':
                type_ = Token.TYPE.EQUEQU
                self._advance()
        # --Symbol: ! | !=
        elif char == '!':
            if self._peek() == '=':
                type_ = Token.TYPE.NOTEQU
                self._advance()
        else:
            type_ = {
                '(': Token.TYPE.LPAREN,
                ')': Token.TYPE.RPAREN,
                ';': Token.TYPE.SEMICOLON,
            }.get(char)
        if not type_:
            raise SyntaxError(f"Unhandled symbol '{char}' in lexer.symbol")
        return Token(self.file_path, pos, type_)

    # -Instance Methods: Public
    def get_next_token(self) -> Token | None:
        '''Get next token from lexer'''
        if not self.fp:
            Lexer.check_unhandled_tokens()
            self.fp = self.file_path.open('r')
        if token := self._lex():
            return token
        self.fp.close()
        return None

    # -Static Methods
    @staticmethod
    def check_unhandled_tokens() -> None:
        '''Checks all unhandled token types in lexer amd throws error if any found'''
        unhandled_token_types: tuple[Token.TYPE, ...] = tuple(
            type_
            for type_ in Token.TYPE
            if type_ not in (
                # -KEYWORD
                # -LITERAL
                Token.TYPE.IDENTIFIER,
                Token.TYPE.NUMBER,
                # -COMPARISON
                Token.TYPE.EQUEQU,
                Token.TYPE.NOTEQU,
                # -SYMBOL
                Token.TYPE.ADD,
                Token.TYPE.SUB,
                Token.TYPE.MUL,
                Token.TYPE.DIV,
                Token.TYPE.MOD,
                Token.TYPE.SEMICOLON,
                Token.TYPE.LPAREN,
                Token.TYPE.RPAREN,
            )
        )
        if not unhandled_token_types:
            return
        raise NotImplementedError(
            "Lexer unable to handle the following tokens: {}".format(
                ", ".join(f"'{type_.name}'" for type_ in unhandled_token_types)
            )
        )

    # -Properties
    @property
    def position(self) -> tuple[int, int]:
        return (self.line, self.column)

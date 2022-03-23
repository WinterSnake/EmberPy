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
SYMBOLS: tuple[str] = (
    # -MATH
    '+', '-', '*', '/', '%',
    # -COMPARISONS
    "==",
    # -OTHER
    '(', ')', '{', '}', ';',
)


## Functions
def lex_file(file_path: Path) -> list[Token]:
    """Parse file and return list of strings"""
    _lexer_check()
    lexemes: list[str] = []
    src: TextIO = file_path.open('r')
    row: int = 1
    col: int = 0
    tcol: int = 0
    buffer: str = ""
    while (char := src.read(1)):
        col += 1
        if char.isspace():
            if buffer:
                token = Token.from_lexeme(file_path, (row, tcol), buffer)
                lexemes.append(token)
                buffer = ""
            if char == '\n':
                row += 1
                col = 0
            continue
        elif char in SYMBOLS:
            if buffer:
                token = Token.from_lexeme(file_path, (row, tcol), buffer)
                lexemes.append(token)
                buffer = ""
            token = Token.from_lexeme(file_path, (row, col), char)
            lexemes.append(token)
            continue
        if not buffer:
            tcol = col
        buffer += char
    src.close()
    return lexemes


def _lexer_check():
    """Checks if all current token types are handled by the lexer"""
    unhandled_token_types: tuple[Token.TYPE] = tuple(
        type_
        for type_ in Token.TYPE
        if type_ not in (
            # -KEYWORD
            # -LITERAL
            Token.TYPE.IDENTIFIER,
            Token.TYPE.NUMBER,
            # -COMPARISON
            Token.TYPE.EQUEQU,
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
        return None
    raise NotImplementedError(
        "Lexer unable to handle the following tokens: {}".format(
            ", ".join(f"'{type_.name}'" for type_ in unhandled_token_types)
        )
    )

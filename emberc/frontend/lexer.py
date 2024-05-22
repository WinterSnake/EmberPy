#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Lexer               ##
##-------------------------------##

## Imports
from pathlib import Path
from typing import cast
from .token import Token

## Constants
__all__: tuple[str] = ("lex",)
SYMBOLS: tuple[str, ...] = (
    '+', '-', '*', '/', '%', '(', ')', ';', '=',
)
MAPPEDSTRINGS: dict[str, Token.Type] = {
    # -Symbols
    '+': Token.Type.SymbolPlus,
    '-': Token.Type.SymbolMinus,
    '*': Token.Type.SymbolAsterisk,
    '/': Token.Type.SymbolSlash,
    '%': Token.Type.SymbolPercent,
    '(': Token.Type.SymbolLParen,
    ')': Token.Type.SymbolRParen,
    ';': Token.Type.SymbolSemicolon,
    '=': Token.Type.SymbolEqual,
    # -Types
    'int32': Token.Type.TypeInt32,
}

## Functions
def lex(file_path: Path) -> list[Token]:
    """Produce a list of tokens from a given source file"""
    tokens: list[Token] = []
    file = file_path.open('r')
    state: str = 'default'
    buffer: str = ""
    position: list[int] = [1, 1, 0]  # -row, column, offset
    token_position: tuple[int, int, int] | None = None
    while (c := file.read(1)):
        # -State[Default]
        if state == 'default':
            if c in SYMBOLS:
                op = MAPPEDSTRINGS.get(c)
                pos = cast(tuple[int, int, int], tuple(position))
                assert(op is not None)
                token = Token(file_path, pos, op, None)
                tokens.append(token)
            elif c.isdigit():
                buffer += c
                state = 'number'
                token_position = cast(tuple[int, int, int], tuple(position))
            elif c.isalpha() or c == '_':
                buffer += c
                state = 'word'
                token_position = cast(tuple[int, int, int], tuple(position))
        # -State[Number]
        elif state == 'number':
            assert(token_position is not None)
            if c in SYMBOLS:
                state = 'default'
                op = MAPPEDSTRINGS.get(c)
                pos = cast(tuple[int, int, int], tuple(position))
                assert(op is not None)
                tokens.extend([
                    Token(file_path, token_position, Token.Type.Integer, buffer),
                    Token(file_path, pos, op, None)
                ])
                buffer = ""
                token_position = None
            elif not c.isdigit():
                state = 'default'
                token = Token(file_path, token_position, Token.Type.Integer, buffer)
                tokens.append(token)
                buffer = ""
                token_position = None
            else:
                buffer += c
        # -State[Word]
        elif state == 'word':
            assert(token_position is not None)
            if c in SYMBOLS:
                state = 'default'
                _type = MAPPEDSTRINGS.get(buffer, Token.Type.Identifier)
                _value = None if _type != Token.Type.Identifier else buffer
                op = MAPPEDSTRINGS.get(c)
                pos = cast(tuple[int, int, int], tuple(position))
                assert(op is not None)
                tokens.extend([
                    Token(file_path, token_position, _type, _value),
                    Token(file_path, pos, op, None)
                ])
                buffer = ""
                token_position = None
            elif not c.isalnum() and c != '_':
                state = 'default'
                _type = MAPPEDSTRINGS.get(buffer, Token.Type.Identifier)
                _value = None if _type != Token.Type.Identifier else buffer
                token = Token(file_path, token_position, _type, _value)
                tokens.append(token)
                buffer = ""
                token_position = None
            else:
                buffer += c
        # -Handle positions
        if c == '\n':
            position[0] += 1
            position[1] = 1
        else:
            position[1] += 1
        position[2] += 1
    file.close()
    return tokens

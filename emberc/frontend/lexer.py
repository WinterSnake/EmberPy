#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Lexer               ##
##-------------------------------##

## Imports
from pathlib import Path
from .token import Token

## Constants
__all__: tuple[str] = ("lex",)
SYMBOLS: tuple[str, ...] = (
    '(', ')', '{', '}',
)
MAPPEDSTRINGS: dict[str, Token.Type] = {
    # -Symbols
    '(': Token.Type.SymbolLParen,
    ')': Token.Type.SymbolRParen,
    '{': Token.Type.SymbolLBracket,
    '}': Token.Type.SymbolRBracket,
    # -Keywords
    'fn': Token.Type.KeywordFunction,
}

## Functions
def lex(file_path: Path) -> list[Token]:
    """Produce a list of tokens from a given source file"""
    tokens: list[Token] = []
    file = file_path.open('r')
    state: str = 'default'
    buffer: str = ""
    position: list[int, int, int] = [1, 1, 0]  # -row, column, offset
    token_position: tuple[int, int, int] | None = None
    while (c := file.read(1)):
        # -State: Default
        if state == 'default':
            # -Handle[Symbol]
            if c in SYMBOLS:
                tokens.append(Token(file_path, tuple(position), MAPPEDSTRINGS.get(c), None))
            # -Transition[word]
            if c.isalpha() or c == '_':
                token_position = tuple(position)
                buffer += c
                state = 'word'
        # -State: Word
        elif state == 'word':
            # -Handle[Symbol]
            if c in SYMBOLS:
                state = 'default'
                token = Token(
                    file_path, token_position,
                    MAPPEDSTRINGS.get(buffer, Token.Type.Identifier),
                    None if buffer in MAPPEDSTRINGS else buffer
                )
                buffer = ""
                token_position = None
                tokens.append(token)
                tokens.append(Token(file_path, tuple(position), MAPPEDSTRINGS.get(c), None))
            # -Transition[Default]
            elif not c.isalnum() and c != '_':
                state = 'default'
                token = Token(
                    file_path, token_position,
                    MAPPEDSTRINGS.get(buffer, Token.Type.Identifier),
                    None if buffer in MAPPEDSTRINGS else buffer
                )
                buffer = ""
                token_position = None
                tokens.append(token)
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

#!/usr/bin/python
##-------------------------------##
## Ember: Frontend               ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Lexer                         ##
##-------------------------------##

## Imports
from pathlib import Path
from typing import TextIO

## Constants
SYMBOLS: tuple[str] = (
    # -MATH
    '+', '-', '*', '/', '%',
    # -OTHER
    '(', ')', ';',
)


## Functions
def lex_file(file_path: Path) -> list[str]:
    """Parse file and return list of strings"""
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
                token = (file_path, row, tcol, buffer)
                lexemes.append(token)
                buffer = ""
            if char == '\n':
                row += 1
                col = 0
            continue
        elif char in SYMBOLS:
            if buffer:
                token = (file_path, row, tcol, buffer)
                lexemes.append(token)
                buffer = ""
            token = (file_path, row, col, char)
            lexemes.append(token)
            continue
        if not buffer:
            tcol = col
        buffer += char
    src.close()
    return lexemes

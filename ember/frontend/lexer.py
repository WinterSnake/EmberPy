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


## Functions
def lex_file(file: Path) -> list[str]:
    """Parse file and return list of strings"""
    lexemes: list[str] = []
    src: TextIO = file.open('r')
    buffer: str = ""
    while (char := src.read(1)):
        if char in ('\n', '\r', '\t', ' '):
            if buffer:
                lexemes.append(buffer)
                buffer = ""
            continue
        elif char in ('(', ')', '{', '}', ':', ';'):
            if buffer:
                lexemes.append(buffer)
                buffer = ""
            lexemes.append(char)
            continue
        buffer += char
    src.close()
    return lexemes

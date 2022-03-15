#!/usr/bin/python
##-------------------------------##
## Ember                         ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
import sys
from pathlib import Path

from frontend.lexer import lex_file

## Constants
# -Errors
ERR_USAGE: int = 64
ERR_INPUT: int = 66

## Functions

## Body
if len(sys.argv) == 1 or len(sys.argv) > 2:
    print("No input file", file=sys.stderr)
    sys.exit(ERR_USAGE)
source: Path = Path(sys.argv[1])
if not source.is_file():
    print(f"File '{source.resolve()}' does not exist or is not a file", file=sys.stderr)
    sys.exit(ERR_INPUT)
lexemes: list[str] = lex_file(source)
print(lexemes)

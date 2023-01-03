#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
import sys
from pathlib import Path
from typing import Any

from frontend.lexer import Lexer
from frontend.parser import Parser
from backend import compile_program, interpret_program

## Constants
FILES: list[Path] = []

## Functions
def main() -> None:
    lexer: Lexer = Lexer.from_file_path("tests/test-00.ember")
    parser: Parser = Parser.from_lexer(lexer)
    ast: list[dict[str, Any]] = parser.parse()
    interpret_program(ast)
    compile_program(ast)


## Body
main()

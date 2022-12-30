#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
import sys

from frontend.lexer import Lexer
from frontend.parser import parse_program
from backend import compile_program, interpret_program


## Functions
def main() -> None:
    lexer: Lexer = Lexer.from_file_path("tests/test-00.ember")
    tokens = lexer.get_tokens()
    ast = parse_program(tokens)
    interpret_program(ast)  # type: ignore
    compile_program(ast)  # type: ignore


## Body
main()

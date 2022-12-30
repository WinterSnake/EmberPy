#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
import sys

from lexer import Lexer
from parser import parse_program
from output import compile_program, simulate_program


## Functions
def main() -> None:
    lexer: Lexer = Lexer.from_file_path("tests/test-00.ember")
    tokens = lexer.get_tokens()
    ast = parse_program(tokens)
    #simulate_program(ast)
    #compile_program(ast)


## Body
main()

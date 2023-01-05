#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
import sys
from pathlib import Path
from typing import Any

from frontend import Lexer, Node, Parser, Token
from backend import compile_ast, interpret_ast
from plugins import graph_ast

## Constants
DUMP_TOKENS: bool = False
DUMP_AST: bool = False
FILE: Path = None  # type: ignore
#FILES: list[Path] = []
MODES: tuple[str, ...] = (
    *(MODE_COMPILE := ("-c", "--compile")),
    *(MODE_INTERPRET := ("-i", "--interpret")),
)

## Functions
def usage() -> None:
    """"""
    print(f"Invalid usage: '{sys.argv[0]} <file.ember> [options]'")


def main() -> int:
    global DUMP_TOKENS, DUMP_AST, FILE
    if len(sys.argv) <= 2:
        usage()
        return 1
    mode: int = None  # type: ignore
    # -Handle arguments
    for arg in sys.argv[1:]:
        # -Dump tokens
        if arg in ("-t", "--dump-tokens"):
            DUMP_TOKENS = True
        # -Dump AST
        elif arg in ("-a", "--dump-ast"):
            DUMP_AST = True
        # -Run mode
        elif arg in MODES:
            mode = 1 if arg in MODE_COMPILE else 2
        # -File
        else:
            FILE = Path(arg)
    # -File checking
    if FILE is None or not FILE.exists() or FILE.is_dir():
        usage()
        print(f"Invalid file '{FILE}'. Must be a valid file and exist")
    # -Lexing
    lexer: Lexer = Lexer(FILE)
    if DUMP_TOKENS:
        tokens: list[Token] = lexer.tokens
        with FILE.with_suffix(".tokens").open('w') as f:
            f.writelines(str(token) + "\n" for token in tokens)
    if not DUMP_AST and mode is None:
        return 0
    # -Parsing
    parser: Parser
    if not DUMP_TOKENS:
        parser = Parser.from_lexer(lexer)
    else:
        parser = Parser.from_list(tokens)
    ast: list[Node] = parser.parse()
    if DUMP_AST:
        graph_ast(ast, FILE)
    if mode is None:
        return 0
    # -Compile
    if mode == 1:
        output = FILE
        compile_ast(ast, output)
        return 0
    # -Interpret
    elif mode == 2:
        exit_code: int = interpret_ast(ast)
        return exit_code
    # -Unknown
    usage()
    print(f"Unknown mode '{mode}' - aborting.")
    return 1


## Body
exit_code: int = main()
sys.exit(exit_code)

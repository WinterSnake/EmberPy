#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
import subprocess
import sys
from pathlib import Path
from typing import Any

from frontend import Lexer, Parser, Token
from backend import compile_program, interpret_program
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
    print(f"Invalid usage: '{sys.argv[0]} <mode> <file.ember>'")


def main() -> int:
    global DUMP_TOKENS, DUMP_AST, FILE
    if len(sys.argv) <= 2:
        usage()
        return 1
    elif sys.argv[1] not in MODES:
        usage()
        return 1
    mode: int = 1 if sys.argv[1] in MODE_COMPILE else 2
    # -Handle arguments
    for arg in sys.argv[2:]:
        # -Dump tokens
        if arg in ("-t", "--dump-tokens"):
            DUMP_TOKENS = True
        # -Dump AST
        elif arg in ("-a", "--dump-ast"):
            DUMP_AST = True
        # -File
        else:
            FILE = Path(arg)
    # -File checking
    if FILE is None:
        usage()
        print("Must have a valid file")
    elif not FILE.exists() or FILE.is_dir():
        usage()
        print(f"Invalid file '{FILE}'")
    # -Lexing
    lexer: Lexer = Lexer(FILE)
    if DUMP_TOKENS:
        tokens: list[Token] = lexer.tokens
        with lexer.file.with_suffix(".tokens.txt").open('w') as f:
            f.writelines(str(token) + "\n" for token in tokens)
    # -Parsing
    parser: Parser = Parser.from_lexer(lexer) if not DUMP_TOKENS else Parser.from_list(tokens)
    ast: list[dict[str, Any]] = parser.parse()
    if DUMP_AST:
        graph_ast(ast, FILE.with_suffix(".dot"))
    # -Interpret
    if mode == 2:
        interpret_program(ast)
        return 0
    # -Compile
    output = FILE.with_suffix(".s")
    compile_program(ast, output)
    subprocess.run(["as", str(output), "-o", str(output.with_suffix('.o'))])
    subprocess.run(["ld", str(output.with_suffix('.o')), "-o", str(output.with_suffix(''))])
    return 0


## Body
exit_code: int = main()
sys.exit(exit_code)

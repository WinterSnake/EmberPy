#!/usr/bin/python
##-------------------------------##
## Ember                         ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
import subprocess
import sys
from pathlib import Path
from typing import Any, cast

from frontend.token import Token
from frontend.lexer import Lexer
from frontend.parser import parse_program
from backend.compile import compile_ast
from backend.interpret import interpret_ast

## Constants
# -CLI Parameters
source: Path = None  #type: ignore
run_mode: int | None = None
dump_ast_graph: bool = False
# -Errors
ERR_USAGE: int = 64
ERR_INPUT: int = 66

## Body
if len(sys.argv) == 1:
    print("No input file", file=sys.stderr)
    sys.exit(ERR_USAGE)
for arg in sys.argv[1:]:
    if arg in ("-c", "--compile") and run_mode is None:
        run_mode = 0
    elif arg in ("-s", "--simulate") and run_mode is None:
        run_mode = 1
    elif arg in ("-g", "--graph-ast"):
        from plugins.graph import graph_ast
        dump_ast_graph = True
    else:
        source = Path(arg)
if not source.is_file():
    print(f"File '{source.resolve()}' does not exist or is not a file", file=sys.stderr)
    sys.exit(ERR_INPUT)
lexer = Lexer(source)
tokens: list[Token] = cast(list[Token], [token for token in lexer])
ast: list[Any] | None = parse_program(tokens)
if dump_ast_graph:
    graph = graph_ast(cast(list[Any], ast), format="png")
    graph.render('out.dot', view=False)
if run_mode is not None:
    if run_mode == 0:
        file = Path("main.asm")
        compile_ast(cast(list[Any], ast), file)
        subprocess.run(["as", "main.asm", "-o", "main.o"])
        subprocess.run(["ld", "main.o", "-e", "__start__", "-o", "main"])
    elif run_mode == 1:
        exit_code: int = interpret_ast(cast(list[Any], ast))
        print(f"Exit code: {exit_code}")
    else:
        raise ValueError(f"Run mode '{run_mode}' unknown.")

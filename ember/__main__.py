#!/usr/bin/python
##-------------------------------##
## Ember                         ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
import sys
from pathlib import Path
from typing import Any

from frontend.lexer import lex_file
from frontend.parser import parse_lexemes
from backend.simulate import simulate_ast
from plugins.graph import graph_ast

## Constants
# -Errors
ERR_USAGE: int = 64
ERR_INPUT: int = 66


## Body
if len(sys.argv) == 1 or len(sys.argv) > 2:
    print("No input file", file=sys.stderr)
    sys.exit(ERR_USAGE)
source: Path = Path(sys.argv[1])
if not source.is_file():
    print(f"File '{source.resolve()}' does not exist or is not a file", file=sys.stderr)
    sys.exit(ERR_INPUT)
lexemes: list[str] = lex_file(source)
ast: Any = parse_lexemes(lexemes)
graph = graph_ast(ast, format="png")
graph.render('out', view=True)
result: int = simulate_ast(ast)
print(f"Result: {result}")

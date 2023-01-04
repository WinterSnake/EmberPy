#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Backends                      ##
##-------------------------------##

## Imports
from .compiler import compile_ast
from .interpreter import interpret_ast

## Constants
__all__: tuple[str, ...] = (
    "compile_ast", "interpret_ast",
)

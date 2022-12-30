#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Backends                      ##
##-------------------------------##

## Imports
from .compiler import compile_program
from .interpreter import interpret_program

## Constants
__all__: tuple[str, ...] = (
    "compile_program", "interpret_program"
)

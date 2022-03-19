#!/usr/bin/python
##-------------------------------##
## Ember: Backend                ##
## Written By: Ryan Smith        ##
##-------------------------------##

## Imports
from .compile import compile_ast
from .interpret import interpret_ast

## Constants
__all__ = [compile_ast, interpret_ast]

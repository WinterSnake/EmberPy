#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Backend                       ##
##-------------------------------##

## Imports
from .interpreter import interpret
from .visitor import NodeVisitor
from .passes import FoldingOptimizationPass

## Constants
__all__: tuple[str, ...] = (
    # -Passes
    "NodeVisitor", "FoldingOptimizationPass",
    # -Backend
    "interpret",
)

#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Backend: Visitor Passes       ##
##-------------------------------##

## Imports
from .optimization_folding import FoldingOptimizationPass

## Constants
__all__: tuple[str, ...] = (
    # -Optimization
    "FoldingOptimizationPass",
)

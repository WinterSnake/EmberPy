#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Backend                       ##
##-------------------------------##

## Imports
from .interpreter import interpret

## Constants
__all__: tuple[str, ...] = ("interpret",)

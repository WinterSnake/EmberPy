##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Core                          ##
##-------------------------------##

## Imports
from .lookahead_buffer import LookaheadBuffer
from .span import Span

## Constants
__all__ = (
    "LITERAL_TYPES",
    "LookaheadBuffer",
    "Span",
)
type LITERAL_TYPES = bool | int | str

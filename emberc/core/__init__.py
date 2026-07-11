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
type LITERAL_VALUE_TYPE = bool | int | str
__all__ = (
    "LITERAL_VALUE_TYPE",
    "LookaheadBuffer",
    "Span",
)

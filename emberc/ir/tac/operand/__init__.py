##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## IR 3AC: Operand               ##
##-------------------------------##

## Imports
from .literal import TACLiteral
from .variable import (
    TACTemporary,
    TACVariable,
)

## Constants
__all__ = (
    "TACAddress",
    "TACOperand",
    "TACLiteral",
    "TACTemporary",
    "TACVariable",
)
type TACAddress = TACTemporary | TACVariable
type TACOperand = TACAddress | TACLiteral

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## x86_64: Instructions          ##
##-------------------------------##

## Imports
from .add import x86Add
from .mov import x86Mov
from .mul import x86Mul
from .sub import x86Sub

## Constants
__all__ = (
    "x86Mov",
    "x86Add",
    "x86Sub",
    "x86Mul",
)

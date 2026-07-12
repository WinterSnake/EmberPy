##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## AST: Operators                ##
##-------------------------------##

## Imports
from enum import IntEnum, auto


## Classes
class AssignOperator(IntEnum):
    """Operators for assignment expressions"""
    Eq = auto()


class BinaryOperator(IntEnum):
    """Operators for binary expressions"""
    Add = auto()
    Sub = auto()
    Mul = auto()
    Div = auto()
    Mod = auto()

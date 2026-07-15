##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## AST: Operators                ##
##-------------------------------##

## Imports
from enum import IntEnum, auto
from typing import assert_never


## Classes
class AssignOperator(IntEnum):
    """Operators for assignment expressions"""
    # -Dunder Methods
    def __str__(self) -> str:
        match self:
            case AssignOperator.Eq:
                return '='
            case _:
                assert_never(self)

    # -Class Properties
    Eq = auto()


class BinaryOperator(IntEnum):
    """Operators for binary expressions"""
    # -Dunder Methods
    def __str__(self) -> str:
        match self:
            case BinaryOperator.Add:
                return '+'
            case BinaryOperator.Sub:
                return '-'
            case BinaryOperator.Mul:
                return '*'
            case BinaryOperator.Div:
                return '/'
            case BinaryOperator.Mod:
                return '%'
            case _:
                assert_never(self)

    # -Class Properties
    Add = auto()
    Sub = auto()
    Mul = auto()
    Div = auto()
    Mod = auto()

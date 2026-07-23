##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## AST: Common                   ##
##-------------------------------##

## Imports
from enum import IntEnum, auto
from typing import assert_never


## Classes
class AssignOperator(IntEnum):
    """Operators for assignment expressions."""
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
    """Operators for binary expressions."""
    # -Dunder Methods
    def __str__(self) -> str:
        match self:
            # -Math
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
            # -Comparisons
            case BinaryOperator.Eq:
                return "=="
            case BinaryOperator.NtEq:
                return "=="
            case BinaryOperator.Lt:
                return '<'
            case BinaryOperator.LtEq:
                return "<="
            case BinaryOperator.Gt:
                return '>'
            case BinaryOperator.GtEq:
                return ">="
            case _:
                assert_never(self)

    # -Class Properties
    # --Math
    Add = auto()
    Sub = auto()
    Mul = auto()
    Div = auto()
    Mod = auto()
    # --Comparisons
    Eq = auto()
    NtEq = auto()
    Lt = auto()
    LtEq = auto()
    Gt = auto()
    GtEq = auto()


class PrimitiveType(IntEnum):
    """Built-in primitive types."""
    # -Dunder Methods
    def __str__(self) -> str:
        match self:
            case PrimitiveType.Void:
                return "void"
            case PrimitiveType.Boolean:
                return "bool"
            case PrimitiveType.Int8:
                return "int8"
            case PrimitiveType.Int16:
                return "int16"
            case PrimitiveType.Int32:
                return "int32"
            case PrimitiveType.Int64:
                return "int64"
            case PrimitiveType.UInt8:
                return "uint8"
            case PrimitiveType.UInt16:
                return "uint16"
            case PrimitiveType.UInt32:
                return "uint32"
            case PrimitiveType.UInt64:
                return "uint64"
            case PrimitiveType.ISize:
                return "isize"
            case PrimitiveType.USize:
                return "usize"
            case _:
                assert_never(self)

    # -Class Properties
    Void = auto()
    Boolean = auto()
    Int8 = auto()
    Int16 = auto()
    Int32 = auto()
    Int64 = auto()
    UInt8 = auto()
    UInt16 = auto()
    UInt32 = auto()
    UInt64 = auto()
    ISize = auto()
    USize = auto()


class UnaryOperator(IntEnum):
    """Operators for unary expressions."""
    # -Dunder Methods
    def __str__(self) -> str:
        match self:
            case UnaryOperator.NumNegate:
                return '-'
            case UnaryOperator.LogNegate:
                return '!'
            case _:
                assert_never(self)

    # -Class Properties
    # --Type--
    # --Expression--
    NumNegate = auto()
    LogNegate = auto()

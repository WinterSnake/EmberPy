#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Node                ##
##-------------------------------##

## Imports
from __future__ import annotations
from abc import ABC, abstractmethod
from enum import IntEnum, auto

## Constants
__all__: tuple[str, ...] = (
    "Node", "NodeBinaryOperator", "NodeLiteral",
)


## Classes
class Node(ABC):
    pass


class NodeBinaryExpression(Node):
    """
    """

    # -Constructor
    def __init__(self, lhs: Node, rhs: Node, _type: NodeBinaryExpression.Type) -> None:
        self.lhs: Node = lhs
        self.rhs: Node = rhs
        self.type: NodeBinaryExpression.Type = _type

    # -Dunder Methods
    def __repr__(self) -> str:
        return f"NodeBinaryExpression(lhs={repr(self.rhs)}, op={self.type.name}, rhs={repr(self.rhs)})"

    def __str__(self) -> str:
        match self.type:
            case NodeBinaryExpression.Type.Add:
                return f"({str(self.lhs)}+{str(self.rhs)})"
            case NodeBinaryExpression.Type.Sub:
                return f"({str(self.lhs)}-{str(self.rhs)})"
            case NodeBinaryExpression.Type.Mul:
                return f"({str(self.lhs)}*{str(self.rhs)})"
            case NodeBinaryExpression.Type.Div:
                return f"({str(self.lhs)}/{str(self.rhs)})"
            case NodeBinaryExpression.Type.Mod:
                return f"({str(self.lhs)}%{str(self.rhs)})"

    # -Sub-Classes
    class Type(IntEnum):
        Add = auto()
        Sub = auto()
        Mul = auto()
        Div = auto()
        Mod = auto()


class NodeLiteral(Node):
    """
    """

    # -Constructor
    def __init__(self, value: int) -> None:
        self.value: int = value

    # -Dunder Methods
    def __repr__(self) -> str:
        return f"NodeLiteral(type=Type.Number, value={repr(self.value)})"

    def __str__(self) -> str:
        return repr(self.value)

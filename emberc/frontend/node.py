#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Node                ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto

## Constants
__all__: tuple[str] = ("Node", "NodeBinExpr", "NodeLiteral",)


## Classes
class Node:
    """"""
    pass


class NodeBinExpr(Node):
    """"""

    # -Constructor
    def __init__(self, _type: NodeBinExpr.Type, lhs: Node, rhs: Node) -> None:
        self.type: NodeBinExpr.Type = _type
        self.lhs: Node = lhs
        self.rhs: Node = rhs

    # -Dunder Methods
    def __repr__(self) -> str:
        return f"NodeBinExpr(type={self.type}, lhs={repr(self.lhs)}, rhs={repr(self.rhs)})"

    def __str__(self) -> str:
        expr: str
        match self.type:
            case NodeBinExpr.Type.Add:
                expr = '+'
            case NodeBinExpr.Type.Sub:
                expr = '-'
            case NodeBinExpr.Type.Mul:
                expr = '*'
            case NodeBinExpr.Type.Div:
                expr = '/'
            case NodeBinExpr.Type.Mod:
                expr = '%'
        return f"({self.lhs}{expr}{self.rhs})"

    # -Sub-Classes
    class Type(IntEnum):
        ''''''
        Add = auto()
        Sub = auto()
        Mul = auto()
        Div = auto()
        Mod = auto()


class NodeLiteral(Node):
    """"""
    
    # -Constructor
    def __init__(self, _type: NodeLiteral.Type, value: int) -> None:
        self.type: NodeLiteral.Type = _type
        self.value: int = value

    # -Dunder Methods
    def __repr__(self) -> str:
        return f"NodeLiteral(type={self.type}, value={repr(self.value)})"

    def __str__(self) -> str:
        return str(self.value)

    # -Sub-Classes
    class Type(IntEnum):
        ''''''
        Integer = auto()

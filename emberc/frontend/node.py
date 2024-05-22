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
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..backend.visitor import NodeVisitor

## Constants
__all__: tuple[str, ...] = ("Node", "NodeBinExpr", "NodeLiteral",)


## Classes
class Node(ABC):
    """"""

    # -Instance Methods
    @abstractmethod
    def visit(self, visitor: NodeVisitor) -> Node: ...


class NodeAssignment(Node):
    """"""

    # -Constructor
    def __init__(self, name: str, value: Node) -> None:
        self.name: str = name
        self.value = value

    # -Dunder Methods
    def __repr__(self) -> str:
        return "NodeAssignment(name={self.name}, value={repr(self.value)})"

    def __str__(self) -> str:
        return f"{self.name}={self.value}"

    # -Instance Methods
    def visit(self, visitor: NodeVisitor) -> Node:
        return visitor.visit_assignment(self)

class NodeDefinition(NodeAssignment):
    """"""

    # -Constructor
    def __init__(self, _type, name: str, value: Node) -> None:
        super().__init__(name, value)
        self.type = _type

    # -Dunder Methods
    def __repr__(self) -> str:
        return "NodeDefinition(type={}, name={self.name}, value={repr(self.value)})"

    def __str__(self) -> str:
        return f"[{self.type}]{self.name}={self.value}"

    # -Instance Methods
    def visit(self, visitor: NodeVisitor) -> Node:
        return visitor.visit_definition(self)


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

    # -Instance Methods
    def visit(self, visitor: NodeVisitor) -> Node:
        return visitor.visit_binexpr(self)

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
    def __init__(self, _type: NodeLiteral.Type, value: int | str) -> None:
        self.type: NodeLiteral.Type = _type
        self.value: int | str = value

    # -Dunder Methods
    def __repr__(self) -> str:
        return f"NodeLiteral(type={self.type}, value={repr(self.value)})"

    def __str__(self) -> str:
        return str(self.value)

    # -Instance Methods
    def visit(self, visitor: NodeVisitor) -> Node:
        return visitor.visit_literal(self)

    # -Sub-Classes
    class Type(IntEnum):
        ''''''
        Identifier = auto()
        Integer = auto()

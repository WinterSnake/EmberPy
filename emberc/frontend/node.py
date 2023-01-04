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
from enum import Enum, auto
from typing import Any


## Classes
class Node(ABC):
    """"""

    # -Instance Methods
    @abstractmethod
    def visit(self, visitor: Node.Visitor, *args) -> Any:
        ''''''
        pass

    # -Sub-classes
    class Visitor(ABC):
        ''''''

        # -Instance Methods
        @abstractmethod
        def visit_expression_node(self, node: ExpressionNode, *args) -> Any:
            ''''''
            pass

        @abstractmethod
        def visit_value_node(self, node: ValueNode, *args) -> Any:
            ''''''
            pass



class ExpressionNode(Node):
    """"""

    # -Constructor
    def __init__(self, operator: ExpressionNode.Type, lhs: Node, rhs: Node) -> None:
        self.operator: ExpressionNode.Type = operator
        self.lhs: Node = lhs
        self.rhs: Node = rhs

    # -Dunder Methods
    def __str__(self) -> str:
        lhs: str = str(self.lhs)
        rhs: str = str(self.rhs)
        match self.operator:
            case ExpressionNode.Type.ADD:
                return f"({lhs} + {rhs})"
            case ExpressionNode.Type.SUB:
                return f"({lhs} - {rhs})"
            case ExpressionNode.Type.MUL:
                return f"({lhs} * {rhs})"
            case ExpressionNode.Type.DIV:
                return f"({lhs} / {rhs})"
            case ExpressionNode.Type.MOD:
                return f"({lhs} % {rhs})"

    # -Instance Methods
    def visit(self, visitor: Node.Visitor, *args) -> Any:
        return visitor.visit_expression_node(self, *args)

    # -Sub-Classes
    class Type(Enum):
        ''''''
        ADD = auto()
        SUB = auto()
        MUL = auto()
        DIV = auto()
        MOD = auto()


class ValueNode(Node):
    """"""

    # -Constructor
    def __init__(self, _type: ValueNode.Type, value: str) -> None:
        self.type: ValueNode.Type = _type
        self.value: str = value

    # -Dunder Methods
    def __str__(self) -> str:
        return self.value

    # -Instance Methods
    def visit(self, visitor: Node.Visitor, *args) -> Any:
        return visitor.visit_value_node(self, *args)

    # -Sub-Classes
    class Type(Enum):
        ''''''
        NUMERIC = auto()

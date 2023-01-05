#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Node                ##
##-------------------------------##

## Imports
from __future__ import annotations
import re
from enum import Enum, auto
from typing import Any, Protocol


## Classes
class Node:
    """AST Base Node Class"""

    # -Instance Methods
    def visit(self, visitor: Node.Visitor) -> Any:
        '''Calls visitor function based on node class name'''
        node: str = "visit" + re.sub(
            r"([A-Z])", lambda pattern: '_' + str(pattern.group(1).lower()),
            self.__class__.__name__
        )
        visit_method = getattr(visitor, node)
        return visit_method(self)

    # -Sub-classes
    class Visitor(Protocol):
        '''Node Visitor Pattern Protocol'''
        # -Instance Methods
        def visit_call_node(self, node: CallNode) -> Any: ...
        def visit_expression_node(self, node: ExpressionNode) -> Any: ...
        def visit_value_node(self, node: ValueNode) -> Any: ...



class CallNode(Node):
    """Temporary DEBUG__PRINT__ call handler Node"""

    # -Constructor
    def __init__(self, argument: Node) -> None:
        self.argument: Node = argument


class ExpressionNode(Node):
    """AST Expression Node"""

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

    # -Sub-Classes
    class Type(Enum):
        '''Binary Expression Node Type'''
        ADD = auto()
        SUB = auto()
        MUL = auto()
        DIV = auto()
        MOD = auto()


class ValueNode(Node):
    """AST Value Node"""

    # -Constructor
    def __init__(self, _type: ValueNode.Type, value: str) -> None:
        self.type: ValueNode.Type = _type
        self.value: str = value

    # -Dunder Methods
    def __str__(self) -> str:
        return self.value

    # -Sub-Classes
    class Type(Enum):
        '''Value Node Type'''
        NUMERIC = auto()

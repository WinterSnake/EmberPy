#!/usr/bin/python
##-------------------------------##
## Ember: Frontend               ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node Structure                ##
##-------------------------------##

## Imports
from abc import ABC, abstractmethod
from enum import IntEnum, auto
from typing import TextIO


## Classes
class NodeBase(ABC):
    """AST Base Node"""
    
    # -Instance Methods
    @abstractmethod
    def compile(self, file: TextIO) -> None:
        '''Compile the current node based to file'''
        pass

    @abstractmethod
    def interpret(self) -> Any:
        '''Interpret the current node'''
        pass


class NodeExpression(Node):
    """AST Expression Node"""

    # -Constructor
    def __init__(
        self, operator: NodeExpression.Operator, lhs: NodeBase, rhs: NodeBase
    ) -> None:
        self.operator: NodeExpression.Operator = operator
        self.lhs: NodeBase = lhs
        self.rhs: NodeBase = rhs
    
    # -Instance Methods
    def compile(self, file: TextIO) -> None:
        pass

    def interpret(self) -> Any:
        pass

    # -Sub-Classes
    class OPERATOR(IntEnum):
        '''Node Expression Operator'''
        ADD = auto()
        SUB = auto()
        MUL = auto()
        DIV = auto()
        MOD = auto()


class NodeLiteral(Node):
    """AST Literal Node"""

    # -Constructor
    def __init__(self, value: int):
        self.value: int = value

    # -Instance Methods
    def compile(self, file: TextIO) -> None:
        pass

    def interpret(self) -> Any:
        pass

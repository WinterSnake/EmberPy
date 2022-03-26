#!/usr/bin/python
##-------------------------------##
## Ember: Frontend               ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node Structure                ##
##-------------------------------##

## Imports
from __future__ import annotations
from abc import ABC, abstractmethod
from enum import IntEnum, auto
from typing import Any, TextIO


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


class NodeStatement(NodeBase):
    """AST Statement Node"""

    # -Constructor
    def __init__(self, expression: NodeExpression) -> None:
        self.expression = expression

    # -Instance Methods
    def compile(self, file: TextIO) -> None:
        self.expression.compile(file)
        file.writelines([
            "# -- DEBUG PRINTU -- #\n",
            "\tpop %rdi\n",
            "\t call DEBUG__PRINTU__\n",
        ])

    def interpret(self) -> None:
        expr = self.expression.interpret()
        print(expr)


class NodeExpression(NodeBase):
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
        self.lhs.compile(file)
        self.rhs.compile(file)
        file.writelines([
           f"# -- {self.operator.name} -- #\n"
            "\tpop %rbx\n",
            "\tpop %rax\n",
        ])
        if self.operator == NodeExpression.OPERATOR.ADD:
            file.writelines([
                "\taddq %rbx, %rax\n",
                "\tpush %rax\n",
            ])
        elif self.operator == NodeExpression.OPERATOR.SUB:
            file.writelines([
                "\tsubq %rbx, %rax\n",
                "\tpush %rax\n",
            ])
        elif self.operator == NodeExpression.OPERATOR.MUL:
            file.writelines([
                "\timulq %rbx, %rax\n",
                "\tpush %rax\n",
            ])
        elif self.operator == NodeExpression.OPERATOR.DIV:
            file.writelines([
                "\tcqto\n",
                "\tidivq %rbx\n",
                "\tpush %rax\n",
            ])
        elif self.operator == NodeExpression.OPERATOR.MOD:
            file.writelines([
                "\tcqto\n",
                "\tidivq %rbx\n",
                "\tpush %rdx\n",
            ])
        elif self.operator == NodeExpression.OPERATOR.EQUEQU:
            file.writelines([
                "\tcmpq %rbx, %rax\n",
                "\tsete %al\n",
            ])

    def interpret(self) -> int:
        lhs: Any = self.lhs.interpret()
        rhs: Any = self.rhs.interpret()
        if self.operator == NodeExpression.OPERATOR.ADD:
            return lhs + rhs
        elif self.operator == NodeExpression.OPERATOR.SUB:
            return lhs - rhs
        elif self.operator == NodeExpression.OPERATOR.MUL:
            return lhs * rhs
        elif self.operator == NodeExpression.OPERATOR.DIV:
            return lhs // rhs
        elif self.operator == NodeExpression.OPERATOR.MOD:
            return lhs % rhs
        elif self.operator == NodeExpression.OPERATOR.EQUEQU:
            return int(lhs == rhs)

    # -Sub-Classes
    class OPERATOR(IntEnum):
        '''Node Expression Operator'''
        ADD = auto()
        SUB = auto()
        MUL = auto()
        DIV = auto()
        MOD = auto()
        EQUEQU = auto()


class NodeLiteral(NodeBase):
    """AST Literal Node"""

    # -Constructor
    def __init__(self, value: int):
        self.value: int = value

    # -Instance Methods
    def compile(self, file: TextIO) -> None:
        file.writelines([
            "# -- push (uint64) -- #\n",
           f"\tpush ${self.value}\n",
        ])

    def interpret(self) -> int:
        return self.value

#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Backend: Interpreter          ##
##-------------------------------##

## Imports
from typing import Any

from frontend import Node, ExpressionNode, ValueNode


## Functions
def interpret_program(program: list[Node]) -> None:
    """"""
    interpreter: InterpreterVisitor = InterpreterVisitor()
    for node in program:
        print(node.visit(interpreter))


## Classes
class InterpreterVisitor(Node.Visitor):
    """"""

    # -Instance Methods
    def visit_expression_node(self, node: ExpressionNode) -> int:
        lhs: int = node.lhs.visit(self)
        rhs: int = node.rhs.visit(self)
        match node.operator:
            case ExpressionNode.Type.ADD:
                return lhs + rhs
            case ExpressionNode.Type.SUB:
                return lhs - rhs
            case ExpressionNode.Type.MUL:
                return lhs * rhs
            case ExpressionNode.Type.DIV:
                return lhs // rhs
            case ExpressionNode.Type.MOD:
                return lhs % rhs
            case _:
                # -TODO: Throw error
                pass

    def visit_value_node(self, node: ValueNode) -> int:
        return int(node.value)

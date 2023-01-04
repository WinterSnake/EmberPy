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
def interpret_ast(nodes: list[Node]) -> int:
    """Use Interpreter Visitor to run AST through Python
    Will return exit code of AST"""
    exit_code: int = 0
    visitor: Node.Visitor = InterpreterVisitor()
    for node in nodes:
        value: int = node.visit(visitor)
        print(value)
    return exit_code


## Classes
class InterpreterVisitor:
    """
    Interpreter AST Visitor
    Interprets and runs python code based on node visited
    """

    # -Instance Methods
    def visit_expression_node(self, node: ExpressionNode) -> int:
        '''Returns binary operation of lhs and rhs numeric values'''
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
        '''Returns basic node to as numeric literal value'''
        return int(node.value)

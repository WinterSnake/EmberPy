##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node Visitor                  ##
##-------------------------------##

## Imports
from __future__ import annotations
from .nodes import (
    LITERAL,
    Node,
    NodeDeclModule,
    NodeStmtExpression,
    NodeExprBinary,
    NodeExprLiteral,
)


## Classes
class Interpreter:
    """
    Ember Interpreter

    Walks through the AST tree and interprets each node
    """
    
    # -Instance Methods
    def visit_declaration_module(self, node: NodeDeclModule) -> None:
        for child in node.nodes:
            child.accept(self)

    def visit_statement_expression(self, node: NodeStmtExpression) -> None:
        value = node.expression.accept(self)
        print(f"Value: {value}")

    def visit_expression_binary(self, node: NodeExprBinary) -> LITERAL:
        lhs = node.lhs.accept(self)
        rhs = node.rhs.accept(self)
        match node.operator:
            case NodeExprBinary.Operator.Add:
                return lhs + rhs
            case NodeExprBinary.Operator.Sub:
                return lhs - rhs
            case NodeExprBinary.Operator.Mul:
                return lhs * rhs
            case NodeExprBinary.Operator.Div:
                return lhs // rhs
            case NodeExprBinary.Operator.Mod:
                return lhs % rhs

    def visit_expression_literal(self, node: NodeExprLiteral) -> LITERAL:
        return node.value

    # -Static Methods
    @staticmethod
    def run(node: Node) -> None:
        interpreter = Interpreter()
        node.accept(interpreter)

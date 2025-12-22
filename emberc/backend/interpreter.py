##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Backend: Interpreter          ##
##-------------------------------##

## Imports
from ..middleware.nodes import (
    NodeDeclUnit,
    NodeExprBinary, NodeExprUnary, NodeExprLiteral
)
from ..middleware.visitor import NodeVisitor

## Constants
__all__ = ("interpreter",)


## Classes
class InterpreterDeclVisitor:
    def visit_unit(self, node, manager) -> None:
        for stmt in node.body:
            manager.visit_statement(stmt)


class InterpreterStmtVisitor:
    def visit_expression(self, node, manager) -> None:
        if node.is_empty:
            return
        value = manager.visit_expression(node.expression)
        print(value)


class InterpreterExprVisitor:
    def visit_group(self, node, manager) -> int:
        return manager.visit_expression(node.expression)

    def visit_binary(self, node, manager) -> int:
        lhs = manager.visit_expression(node.lhs)
        rhs = manager.visit_expression(node.rhs)
        match node.operator:
            case NodeExprBinary.Operator.Add: return lhs + rhs
            case NodeExprBinary.Operator.Sub: return lhs - rhs
            case NodeExprBinary.Operator.Mul: return lhs * rhs
            case NodeExprBinary.Operator.Div: return lhs // rhs
            case NodeExprBinary.Operator.Mod: return lhs % rhs
            case _: raise RuntimeError(f"Unimplemented interpreter binary operator {node.operator.name}")

    def visit_unary(self, node, manager) -> int:
        value = manager.visit_expression(node.expression)
        match node.operator:
            case NodeExprUnary.Operator.Negative: return -value
            case _: raise RuntimeError(f"Unimplemented interpreter unary operator {node.operator.name}")

    def visit_literal(self, node, manager) -> int:
        match node.type:
            case NodeExprLiteral.Type.Integer: return node.value
            case _: raise RuntimeError(f"Unimplemented interpreter literal {node.type.name}")


## Body
interpreter = NodeVisitor(
    InterpreterDeclVisitor(),
    InterpreterStmtVisitor(),
    InterpreterExprVisitor()
)

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
    NodeDeclModule, NodeDeclVariable,
    NodeStmtAssignment, NodeStmtExpression,
    NodeExprBinary,
    NodeExprGroup, NodeExprLiteral,
)
from ..errors import DebugLevel


## Classes
class Interpreter:
    """
    Ember Interpreter

    Walks through the AST tree and interprets each node
    """

    # -Constructor
    def __init__(self) -> None:
        self.debug_level: DebugLevel = DebugLevel.Off
        # -Environment
        self.environments: list[dict[str, LITERAL]] = [{}]
    
    # -Instance Methods
    def visit_declaration_module(self, node: NodeDeclModule) -> None:
        if self.debug_level <= DebugLevel.Info:
            print(f"[Interpreter::Declaration::Module]")
        for child in node.nodes:
            child.accept(self)

    def visit_declaration_variable(self, node: NodeDeclVariable) -> None:
        value: LITERAL | None = None
        if node.initializer is not None:
            value = node.initializer.accept(self)
        if self.debug_level <= DebugLevel.Info:
            print(f"[Interpreter::Declaration::Variable] {node.id} = {value}")
        env = self.current
        env[node.id] = value  # type: ignore

    def visit_statement_assignment(self, node: NodeStmtAssignment) -> None:
        value = node.expression.accept(self)
        if self.debug_level <= DebugLevel.Info:
            print(f"[Interpreter::Statement::Assignment] {node.id} = {value}")
        env = self.current
        env[node.id] = value

    def visit_statement_expression(self, node: NodeStmtExpression) -> None:
        if self.debug_level <= DebugLevel.Info:
            print(f"[Interpreter::Statement::Expression]")
        value = node.expression.accept(self)
        print(f"Value: {value}")

    def visit_expression_binary(self, node: NodeExprBinary) -> LITERAL:
        if self.debug_level <= DebugLevel.Info:
            print(f"[Interpreter::Expression::Binary] {node.operator.name}")
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

    def visit_expression_group(self, node: NodeExprGroup) -> LITERAL:
        if self.debug_level <= DebugLevel.Info:
            print(f"[Interpreter::Expression::Group]")
        return node.expression.accept(self)

    def visit_expression_literal(self, node: NodeExprLiteral) -> LITERAL:
        if self.debug_level <= DebugLevel.Info:
            print(f"[Interpreter::Expression::Literal] {node.value}")
        return node.value

    # -Static Methods
    @staticmethod
    def run(node: Node, debug_level: DebugLevel = DebugLevel.Off) -> None:
        interpreter = Interpreter()
        interpreter.debug_level = debug_level
        node.accept(interpreter)

    # -Properties
    @property
    def current(self) -> dict[str, LITERAL]:
        return self.environments[-1]

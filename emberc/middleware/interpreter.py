##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Middleware: Interpreter       ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import Any
from .nodes import (
    Node, NodeModule, NodeStmtBlock, NodeStmtConditional, NodeStmtLoop,
    NodeDeclVariable, NodeStmtExpression, NodeExprAssignment,
    NodeExprBinary, NodeExprUnary, 
    NodeExprGroup, NodeExprVariable, NodeExprLiteral
)

## Constants
ENVIRONMENT: dict[str, bool | int | None]


## Classes
class InterpreterVisitor:
    """AST Traversal Pass: Interpreter"""

    # -Constructor
    def __init__(self, debug_mode: bool) -> None:
        self.debug_mode: bool = debug_mode
        self.environments: list[ENVIRONMENT] = [{}]

    # -Instance Methods: Environment
    def pop(self) -> None:
        '''Pop last environment on the stack'''
        if self.debug_mode:
            print("Pop environment")
        self.environments.pop()

    def push(self) -> None:
        '''Push new environment on the stack'''
        if self.debug_mode:
            print("Push environment")
        self.environments.append({})

    def _get_variable(self, _id: str) -> bool | int | None:
        '''Iterate through each environment and return id value from closest to stack'''
        for env in reversed(self.environments):
            if _id in env:
                return env[_id]
        return None

    def _get_variable_environment(self, _id: str) -> ENVIRONMENT | None:
        '''Iterate through each environment and return id location from closest to stack'''
        for env in reversed(self.environments):
            if _id in env:
                return env
        return None

    # -Instance Methods: Visitor
    def visit_module(self, node: NodeModule) -> None:
        if self.debug_mode:
            print(f"[Interpreter::Module]")
        for child in node.body:
            child.accept(self)

    def visit_declaration_variable(self, node: NodeDeclVariable) -> None:
        environment = self.current_environment
        value = None if node.initializer is None else node.initializer.accept(self)
        if self.debug_mode:
            print(f"{{Interpreter::Decl::Var}}Id({node.id}) = {value}")
        environment[node.id] = value

    def visit_statement_block(self, node: NodeStmtBlock) -> None:
        if self.debug_mode:
            print(f"[Interpreter::Stmt::Block]")
        self.push()
        for child in node.body:
            child.accept(self)
        self.pop()

    def visit_statement_conditional(self, node: NodeStmtConditional) -> None:
        if self.debug_mode:
            print(f"[Interpreter::Stmt::Conditional]")
        if node.condition.accept(self):
            node.body.accept(self)
        else:
            if node.branch is None:
                return
            node.branch.accept(self)

    def visit_statement_loop(self, node: NodeStmtLoop) -> None:
        if self.debug_mode:
            print(f"[Interpreter::Stmt::Loop]")
        while node.condition.accept(self):
            node.body.accept(self)

    def visit_statement_expression(self, node: NodeStmtExpression) -> None:
        value = node.expression.accept(self)
        print(value)

    def visit_expression_assignment(self, node: NodeExprAssignment) -> bool | int:
        if self.debug_mode:
            print(f"{{Interpreter::Stmt::Assignment}}[{node.location}]{node}")
        environment = self._get_variable_environment(node.id)
        assert environment is not None
        value = node.expression.accept(self)
        environment[node.id] = value
        return value

    def visit_expression_binary(self, node: NodeExprBinary) -> bool | int:
        if self.debug_mode:
            print(f"{{Interpreter::Stmt::Binary}}[{node.location}]{node}")
        lhs = node.lhs.accept(self)
        rhs = node.rhs.accept(self)
        match node.operator:
            case NodeExprBinary.Type.Add:
                return lhs + rhs
            case NodeExprBinary.Type.Sub:
                return lhs - rhs
            case NodeExprBinary.Type.Mul:
                return lhs * rhs
            case NodeExprBinary.Type.Div:
                return lhs / rhs
            case NodeExprBinary.Type.Mod:
                return lhs % rhs
            case NodeExprBinary.Type.Lt:
                return lhs < rhs
            case NodeExprBinary.Type.Gt:
                return lhs > rhs
            case NodeExprBinary.Type.LtEq:
                return lhs <= rhs
            case NodeExprBinary.Type.GtEq:
                return lhs >= rhs
            case NodeExprBinary.Type.EqEq:
                return lhs == rhs
            case NodeExprBinary.Type.NtEq:
                return lhs != rhs

    def visit_expression_unary(self, node: NodeExprUnary) -> bool | int:
        if self.debug_mode:
            print(f"{{Interpreter::Stmt::Unary}}[{node.location}]{node}")
        value = node.expression.accept(self)
        match node.operator:
            case NodeExprUnary.Type.Negate:
                return not value
            case NodeExprUnary.Type.Negative:
                return -value

    def visit_expression_group(self, node: NodeExprGroup) -> bool | int:
        if self.debug_mode:
            print(f"{{Interpreter::Stmt::Group}}[{node.location}]{node}")
        return node.expression.accept(self)

    def visit_expression_variable(self, node: NodeExprVariable) -> bool | int:
        if self.debug_mode:
            print(f"{{Interpreter::Stmt::Variable}}[{node.location}]{node}")
        value = self._get_variable(node.id)
        assert value is not None
        return value

    def visit_expression_literal(self, node: NodeExprLiteral) -> bool | int:
        if self.debug_mode:
            print(f"{{Interpreter::Stmt::Literal}}[{node.location}]{node}")
        return node.value

    # -Static Methods
    @staticmethod
    def run(node: Node, debug_mode: bool = False):
        interpreter = InterpreterVisitor(debug_mode)
        node.accept(interpreter)

    # -Properties
    @property
    def current_environment(self) -> ENVIRONMENT:
        return self.environments[-1]

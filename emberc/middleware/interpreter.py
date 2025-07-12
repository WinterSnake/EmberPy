##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Middleware: Interpreter       ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Callable, Sequence
from typing import Any, Protocol, Type
from .nodes import (
    Node, NodeModule, NodeDeclFunction, NodeDeclVariable,
    NodeStmtBlock, NodeStmtConditional, NodeStmtLoop, NodeStmtReturn,
    NodeStmtExpression, NodeExprAssignment, NodeExprCall,
    NodeExprBinary, NodeExprUnary, NodeExprGroup,
    NodeExprVariable, NodeExprLiteral
)


## Classes
class EmberCallable(Protocol):
    # -Instance Methods
    def call(
        self, interpreter: InterpreterVisitor, *args: LITERAL
    ) -> LITERAL | None: ...

    # -Properties
    arity: int


class SystemCallable:
    # -Constructor
    def __init__(self, func: Callable[..., Any], arity: int) -> None:
        self.func: Callable[..., Any] = func
        self.arity: int = arity

    # -Instance Methods
    def call(
        self, interpreter: InterpreterVisitor, *arguments: LITERAL
    ) -> LITERAL | None:
        if not arguments:
            return self.func()
        return self.func(*arguments)


class EmberFunction:
    # -Constructor
    def __init__(
        self, parameters: Sequence[str] | None, body: Sequence[Node]
    ) -> None:
        self.parameters: Sequence[str] | None = parameters
        self.body: Sequence[Node] = body
        self.arity: int = len(parameters) if parameters is not None else 0

    # -Instance Methods
    def call(
        self, interpreter: InterpreterVisitor, *arguments: LITERAL
    ) -> LITERAL | None:
        interpreter.push_call_stack()
        environment = interpreter.current_environment
        call_stack = interpreter.current_call_stack
        assert call_stack is not None
        if self.parameters:
            for parameter, argument in zip(self.parameters, arguments):
                environment[parameter] = argument
        for child in self.body:
            child.accept(interpreter)
            if call_stack['exit']:
                break
        return interpreter.pop_call_stack()


class InterpreterVisitor:
    """AST Traversal Pass: Interpreter"""

    # -Constructor
    def __init__(self, debug_mode: bool) -> None:
        self.debug_mode: bool = debug_mode
        self.environments: list[ENVIRONMENT] = [{
            'print': SystemCallable(print, -1)
        }]
        self.call_stack: list[CALL_STACK] = []

    # -Instance Methods: Environment
    def pop_call_stack(self) -> LITERAL | None:
        '''Pop last call stack from interpreter and return value'''
        if self.debug_mode:
            print("\tPop call stack")
        call_stack = self.call_stack.pop()
        self.pop_env()
        return call_stack['value']

    def pop_env(self) -> None:
        '''Pop last environment on the stack'''
        if self.debug_mode:
            print("\tPop environment")
        self.environments.pop()

    def push_call_stack(self) -> None:
        '''Push new call stack into interpreter'''
        if self.debug_mode:
            print("\tPush call stack")
        self.push_env()
        self.call_stack.append({
            'exit': False,
            'value': None,
        })

    def push_env(self) -> None:
        '''Push new environment on the stack'''
        if self.debug_mode:
            print("\tPush environment")
        self.environments.append({})

    def _get_variable(self, _id: str) -> LITERAL | None:
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

    def visit_declaration_function(self, node: NodeDeclFunction) -> None:
        environment = self.current_environment
        environment[node.id] = EmberFunction(node.parameters, node.body)

    def visit_declaration_variable(self, node: NodeDeclVariable) -> None:
        environment = self.current_environment
        value = None if node.initializer is None else node.initializer.accept(self)
        if self.debug_mode:
            print(f"{{Interpreter::Decl::Var}}Id({node.id}) = {value}")
        environment[node.id] = value

    def visit_statement_block(self, node: NodeStmtBlock) -> None:
        if self.debug_mode:
            print(f"[Interpreter::Stmt::Block]")
        call_stack = self.current_call_stack
        self.push_env()
        for child in node.body:
            child.accept(self)
            if call_stack is not None and call_stack['exit']:
                break
        self.pop_env()

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
        call_stack = self.current_call_stack
        while node.condition.accept(self):
            node.body.accept(self)
            if call_stack is not None and call_stack['exit']:
                break

    def visit_statement_return(self, node: NodeStmtReturn) -> None:
        if self.debug_mode:
            print(f"[Interpreter::Stmt::Return]")
        value: LITERAL | None = None
        if node.expression is not None:
            value = node.expression.accept(self)
        call_stack = self.current_call_stack
        if call_stack is None:
            print(f"Error: Invalid return statement")
        else:
            call_stack['exit'] = True
            call_stack['value'] = value

    def visit_statement_expression(self, node: NodeStmtExpression) -> None:
        if self.debug_mode:
            print(f"{{Interpreter::Stmt::Expression}}")
        node.expression.accept(self)

    def visit_expression_assignment(self, node: NodeExprAssignment) -> LITERAL:
        if self.debug_mode:
            print(f"{{Interpreter::Expr::Assignment}}[{node.location}]{node}")
        environment = self._get_variable_environment(node.id)
        assert environment is not None
        value = node.expression.accept(self)
        environment[node.id] = value
        return value

    def visit_expression_binary(self, node: NodeExprBinary) -> LITERAL:
        if self.debug_mode:
            print(f"{{Interpreter::Expr::Binary}}[{node.location}]{node}")
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
                return lhs // rhs
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

    def visit_expression_unary(self, node: NodeExprUnary) -> LITERAL:
        if self.debug_mode:
            print(f"{{Interpreter::Expr::Unary}}[{node.location}]{node}")
        value = node.expression.accept(self)
        match node.operator:
            case NodeExprUnary.Type.Negate:
                return not value
            case NodeExprUnary.Type.Negative:
                return -value

    def visit_expression_call(self, node: NodeExprCall) -> LITERAL | None:
        if self.debug_mode:
            print(f"{{Interpreter::Expr::Call}}[{node.location}]{node}")
        callee = node.callee.accept(self)
        if callee.arity >= 0 and callee.arity != node.argument_count:
            print(f"Error: Invalid invoke {callee}, expected: {callee.arity}; got: {node.argument_count}")
            return None
        if node.has_arguments:
            assert node.arguments is not None
            arguments = tuple(argument.accept(self) for argument in node.arguments)
            return callee.call(self, *arguments)
        return callee.call(self)

    def visit_expression_group(self, node: NodeExprGroup) -> LITERAL:
        if self.debug_mode:
            print(f"{{Interpreter::Expr::Group}}[{node.location}]{node}")
        return node.expression.accept(self)

    def visit_expression_variable(self, node: NodeExprVariable) -> LITERAL:
        if self.debug_mode:
            print(f"{{Interpreter::Expr::Variable}}[{node.location}]{node}")
        value = self._get_variable(node.id)
        assert value is not None
        return value

    def visit_expression_literal(self, node: NodeExprLiteral) -> LITERAL:
        if self.debug_mode:
            print(f"{{Interpreter::Expr::Literal}}[{node.location}]{node}")
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

    @property
    def current_call_stack(self) -> CALL_STACK | None:
        if self.call_stack is None:
            return None
        return self.call_stack[-1]


## Body
LITERAL = bool | int | EmberCallable
ENVIRONMENT = dict[str, LITERAL | None]
CALL_STACK = dict[str, bool | LITERAL | None]

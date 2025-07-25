##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Walker: Interpreter           ##
##-------------------------------##

## Imports
from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Sequence
from ..nodes import (
    LITERAL,
    Node,
    NodeDeclModule, NodeDeclFunction, NodeDeclVariable,
    NodeStmtBlock, NodeStmtCondition, NodeStmtLoop, NodeStmtReturn,
    NodeStmtExpression,
    NodeExprAssignment, NodeExprBinary, NodeExprUnary, NodeExprCall,
    NodeExprGroup, NodeExprVariable, NodeExprLiteral,
)
from ..symbol_table import SymbolTable

## Constants
type ENV_LITERAL = LITERAL | EmberCallable


## Classes
class EmberCallable(ABC):
    
    # -Dunder Methods
    @abstractmethod
    def __call__(
        self, interpreter: InterpreterWalker, *args: LITERAL
    ) -> LITERAL | None: ...

    # -Properties
    @property
    @abstractmethod
    def arity(self) -> int: ...


class EmberFunction(EmberCallable):
    
    # -Constructor
    def __init__(
        self, parameters: Sequence[int] | None, body: Sequence[Node]
    ) -> None:
        self._parameters: Sequence[int] | None = parameters
        self.body: Sequence[Node] = body

    # -Dunder Methods
    def __call__(
        self, interpreter: InterpreterWalker, *args: LITERAL
    ) -> LITERAL | None:
        for child in self.body:
            child.accept(interpreter)
        return None

    # -Properties
    @property
    def arity(self) -> int:
        if self._parameters is None:
            return 0
        return len(self._parameters)


class InterpreterWalker:
    """
    Interpreter Walker

    Walks through the AST tree and interprets the nodes
    """

    # -Constructor
    def __init__(self, table: SymbolTable) -> None:
        # -Environment
        self._table = table
        self._environments: list[dict[str, ENV_LITERAL]] = [{}]

    # -Instance Methods: Visitor
    def visit_declaration_module(self, node: NodeDeclModule) -> None:
        for child in node.body:
            child.accept(self)

    def visit_declaration_function(self, node: NodeDeclFunction) -> None:
        env = self.current_environment
        entry = self._table.lookup(node.id)
        function = EmberFunction(node._parameters, node.body)
        env[entry.name] = function

    def visit_declaration_variable(self, node: NodeDeclVariable) -> None:
        env = self.current_environment
        entry = self._table.lookup(node.id)
        value: LITERAL = None  # type: ignore
        if node.has_initializer:
            value = node.initializer.accept(self)
        env[entry.name] = value

    def visit_statement_block(self, node: NodeStmtBlock) -> None:
        for child in node.body:
            child.accept(self)

    def visit_statement_condition(self, node: NodeStmtCondition) -> None:
        condition = node.condition.accept(self)
        if condition:
            node.body.accept(self)
        elif node.has_branch:
            node.branch.accept(self)

    def visit_statement_loop(self, node: NodeStmtLoop) -> None:
        while node.condition.accept(self):
            node.body.accept(self)

    def visit_statement_return(self, node: NodeStmtReturn) -> None:
        pass

    def visit_statement_expression(self, node: NodeStmtExpression) -> None:
        value = node.expression.accept(self)
        print(f"Value: {value}")

    def visit_expression_assignment(self, node: NodeExprAssignment) -> LITERAL:
        assert isinstance(node.l_value, NodeExprVariable)
        env = self.current_environment
        entry = self._table.lookup(node.l_value.id)
        value = node.r_value.accept(self)
        env[entry.name] = value
        return value

    def visit_expression_binary(self, node: NodeExprBinary) -> LITERAL:
        lhs: ENV_LITERAL = node.lhs.accept(self)
        rhs: ENV_LITERAL = node.rhs.accept(self)
        assert not isinstance(lhs, EmberCallable)
        assert not isinstance(rhs, EmberCallable)
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
            case NodeExprBinary.Operator.Lt:
                return lhs < rhs
            case NodeExprBinary.Operator.Gt:
                return lhs > rhs
            case NodeExprBinary.Operator.LtEq:
                return lhs <= rhs
            case NodeExprBinary.Operator.GtEq:
                return lhs >= rhs
            case NodeExprBinary.Operator.EqEq:
                return lhs == rhs
            case NodeExprBinary.Operator.NtEq:
                return lhs != rhs

    def visit_expression_unary(self, node: NodeExprUnary) -> LITERAL:
        expression = node.expression.accept(self)
        match node.operator:
            case NodeExprUnary.Operator.Negate:
                return not expression
            case NodeExprUnary.Operator.Minus:
                return -expression

    def visit_expression_call(self, node: NodeExprCall) -> LITERAL | None:
        callee = node.callee.accept(self)
        assert isinstance(callee, EmberCallable)
        return callee(self)

    def visit_expression_group(self, node: NodeExprGroup) -> LITERAL:
        return node.expression.accept(self)

    def visit_expression_variable(self, node: NodeExprVariable) -> ENV_LITERAL:
        env = self.current_environment
        entry = self._table.lookup(node.id)
        return env[entry.name]

    def visit_expression_literal(self, node: NodeExprLiteral) -> LITERAL:
        return node.value

    # -Static Methods
    @staticmethod
    def run(node: Node, table: SymbolTable) -> None:
        visitor = InterpreterWalker(table)
        node.accept(visitor)

    # -Properties
    @property
    def current_environment(self) -> dict[str, ENV_LITERAL]:
        return self._environments[-1]

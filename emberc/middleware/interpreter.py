##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Tree Walker: Interpreter      ##
##-------------------------------##

## Imports
from __future__ import annotations
from .nodes import (
    LITERAL,
    Node,
    NodeDeclModule, NodeDeclFunction, NodeDeclVariable,
    NodeStmtBlock, NodeStmtExpression,
    NodeExprBinary,
    NodeExprGroup, NodeExprVariable, NodeExprLiteral,
)
from .symbol_table import SymbolTable
from ..errors import DebugLevel


## Classes
class Interpreter:
    """
    Ember Interpreter

    Walks through the AST tree and interprets each node
    """

    # -Constructor
    def __init__(self, table: SymbolTable) -> None:
        self.debug_level: DebugLevel = DebugLevel.Off
        # -Environment
        self._table: SymbolTable = table
        self.environments: list[dict[str, LITERAL]] = [{}]
    
    # -Instance Methods
    def visit_declaration_module(self, node: NodeDeclModule) -> None:
        if self.debug_level <= DebugLevel.Info:
            print(f"[Interpreter::Declaration::Module]")
        for child in node.body:
            child.accept(self)

    def visit_declaration_function(self, node: NodeDeclFunction) -> None:
        entry = self._table.lookup(node.id)
        if self.debug_level <= DebugLevel.Info:
            print(f"[Interpreter::Declaration::Function] {entry}")
        for child in node.body:
            child.accept(self)

    def visit_declaration_variable(self, node: NodeDeclVariable) -> None:
        entry = self._table.lookup(node.id)
        value: LITERAL = None  # type: ignore
        if node.has_initializer:
            value = node.initializer.accept(self)
        if self.debug_level <= DebugLevel.Info:
            print(f"[Interpreter::Declaration::Variable] {entry} = {value}")
        env = self.current
        env[entry] = value

    def visit_statement_block(self, node: NodeStmtBlock) -> None:
        if self.debug_level <= DebugLevel.Info:
            print(f"[Interpreter::Statement::Block]")
        for child in node.body:
            child.accept(self)

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

    def visit_expression_group(self, node: NodeExprGroup) -> LITERAL:
        if self.debug_level <= DebugLevel.Info:
            print(f"[Interpreter::Expression::Group]")
        return node.expression.accept(self)

    def visit_expression_variable(self, node: NodeExprVariable) -> LITERAL:
        if self.debug_level <= DebugLevel.Info:
            print(f"[Interpreter::Expression::Variable] {node.id}")
        env = self.current
        entry = self._table.lookup(node.id)
        return env[entry]

    def visit_expression_literal(self, node: NodeExprLiteral) -> LITERAL:
        if self.debug_level <= DebugLevel.Info:
            print(f"[Interpreter::Expression::Literal] {node.value}")
        return node.value

    # -Static Methods
    @staticmethod
    def run(
        node: Node, table: SymbolTable,
        debug_level: DebugLevel = DebugLevel.Off
    ) -> None:
        interpreter = Interpreter(table)
        interpreter.debug_level = debug_level
        node.accept(interpreter)

    # -Properties
    @property
    def current(self) -> dict[str, LITERAL]:
        return self.environments[-1]

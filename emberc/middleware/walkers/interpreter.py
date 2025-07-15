##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Walker: Interpreter           ##
##-------------------------------##

## Imports
from ..nodes import (
    LITERAL,
    Node,
    NodeDeclModule, NodeDeclFunction, NodeDeclVariable,
    NodeStmtBlock, NodeStmtExpression,
    NodeExprBinary,
    NodeExprGroup, NodeExprVariable, NodeExprLiteral,
)
from ..symbol_table import SymbolTable


## Classes
class InterpreterWalker:
    """
    Interpreter Walker

    Walks through the AST tree and interprets the nodes
    """

    # -Constructor
    def __init__(self, table: SymbolTable) -> None:
        # -Environment
        self._table = table
        self._environments: list[dict[str, LITERAL]] = [{}]

    # -Instance Methods: Visitor
    def visit_declaration_module(self, node: NodeDeclModule) -> None:
        for child in node.body:
            child.accept(self)

    def visit_declaration_function(self, node: NodeDeclFunction) -> None:
        for child in node.body:
            child.accept(self)

    def visit_declaration_variable(self, node: NodeDeclVariable) -> None:
        env = self.current_environment
        entry = self._table.lookup(node.id)
        value: LITERAL = None  # type: ignore
        if node.has_initializer:
            value = node.initializer.accept(self)
        env[entry] = value

    def visit_statement_block(self, node: NodeStmtBlock) -> None:
        for child in node.body:
            child.accept(self)

    def visit_statement_expression(self, node: NodeStmtExpression) -> None:
        value = node.expression.accept(self)
        print(f"Value: {value}")

    def visit_expression_binary(self, node: NodeExprBinary) -> LITERAL:
        lhs: LITERAL = node.lhs.accept(self)
        rhs: LITERAL = node.rhs.accept(self)
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
        return node.expression.accept(self)

    def visit_expression_variable(self, node: NodeExprVariable) -> LITERAL:
        env = self.current_environment
        entry = self._table.lookup(node.id)
        return env[entry]

    def visit_expression_literal(self, node: NodeExprLiteral) -> LITERAL:
        return node.value

    # -Static Methods
    @staticmethod
    def run(node: Node, table: SymbolTable) -> None:
        visitor = InterpreterWalker(table)
        node.accept(visitor)

    # -Properties
    @property
    def current_environment(self) -> dict[str, LITERAL]:
        return self._environments[-1]

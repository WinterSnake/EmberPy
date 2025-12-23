##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Visitor: Printer              ##
##-------------------------------##

## Imports
from typing import Any
from .nodes import (
    NodeType,
    NodeTypeBuiltin, NodeTypeIdentifier,
    NodeDeclUnit, NodeDeclFunction, NodeDeclVariable,
    NodeStmtBlock, NodeStmtConditional, NodeStmtLoop,
    NodeStmtReturn, NodeStmtExpression,
    NodeExprAssignment, NodeExprGroup, NodeExprBinary, NodeExprUnary,
    NodeExprCall, NodeExprVariable, NodeExprLiteral,
)
from .symbol_table import SymbolTable
from .visitor import NodeVisitor

## Constants
__all__ = ("printer",)
UNARY_OPERATOR = {
    NodeExprUnary.Operator.Negate: '!',
    NodeExprUnary.Operator.Negative: '-',
}
BINARY_OPERATOR = {
    NodeExprBinary.Operator.Add: '+',
    NodeExprBinary.Operator.Sub: '-',
    NodeExprBinary.Operator.Mul: '*',
    NodeExprBinary.Operator.Div: '/',
    NodeExprBinary.Operator.Mod: '%',
    NodeExprBinary.Operator.Lt: '<',
    NodeExprBinary.Operator.Gt: '>',
    NodeExprBinary.Operator.LtEq: '<=',
    NodeExprBinary.Operator.GtEq: '>=',
    NodeExprBinary.Operator.EqEq: '==',
    NodeExprBinary.Operator.NtEq: '!=',
}


## Classes
class NodePrinter(NodeVisitor[str, str, str, str]):
    """
    Node Printer

    A pretty printer for all AST nodes
    """

    # -Constructor
    def __init__(self, symbol_table: SymbolTable, use_lookup: bool = True) -> None:
        super().__init__(self, self, self, self)
        self._symbol_table = symbol_table
        self._indent_level: int = 0

    # -Instance Methods
    def _get_indent(self) -> str:
        return ' ' * self._indent_level

    def _get_node_name(self, node: Any) -> str:
        if self._use_lookup:
            if isinstance(node._id, str):
                return f"'string:{node.name}'"
            else:
                return self._symbol_table.get(node.id).name
        return node.name

    def visit_type_builtin(self, node: NodeTypeBuiltin, manager) -> str:
        return f"[Builtin:{node.type.name}]"

    def visit_type_custom(self, node: NodeTypeIdentifier, manager) -> str:
        symbol = self._symbol_table.get(node.id)
        return f"[Type:{symbol.name}]"

    def visit_decl_unit(self, node: NodeDeclUnit, manager) -> str:
        lines = []
        for decl in node.body:
            lines.append(self.visit(decl))
        return '\n'.join(lines)

    def visit_decl_function(self, node: NodeDeclFunction, manager) -> str:
        name = self._get_node_name(node)
        header = f"{self._get_indent()}{name}("
        parameters = ','.join(self.visit_declaration(parameter) for parameter in node.parameters)
        ret = self.visit_type(node.type)
        body = self.visit_statement(node.body)
        return f"{header}{parameters}):{ret}\n{body}"

    def visit_decl_variable(self, node: NodeDeclVariable, manager) -> str:
        name = self._get_node_name(node)
        _type = self.visit_type(node.type)
        decl = f"{self._get_indent()}{{{_type}{name}"
        if node.has_initializer:
            decl += f" = {self.visit_expression(node.initializer)}"
        return decl + '}'

    def visit_stmt_block(self, node: NodeStmtBlock, manager) -> str:
        header = f"{self._get_indent()}{{"
        self._indent_level += 1
        body = '\n'.join(self.visit(elem) for elem in node.body)
        self._indent_level -= 1
        footer = f"{self._get_indent()}}}"
        return f"{header}\n{body}\n{footer}"

    def visit_stmt_conditional(self, node: NodeStmtConditional, manager) -> str:
        cond = self.visit_expression(node.condition)
        body = self.visit_statement(node.then_branch)
        block = f"{self._get_indent()}if({cond})\n{body}\n"
        if node.has_else_branch:
            else_body = self.visit_statement(node.else_branch)
            block += f"{self._get_indent()}else\n{else_body}"
        return block

    def visit_stmt_loop(self, node: NodeStmtLoop, manager) -> str:
        cond = self.visit_expression(node.condition)
        body = self.visit_statement(node.body)
        return f"{self._get_indent()}while({cond})\n{body}"

    def visit_stmt_return(self, node: NodeStmtReturn, manager) -> str:
        header = f"{self._get_indent()}ret["
        if node.has_value:
            return header + f"{self.visit_expression(node.value)}]"
        return header + "void]"

    def visit_stmt_expression(self, node: NodeStmtExpression, manager) -> str:
        return self._get_indent() + self.visit_expression(node.expression)

    def visit_expr_assignment(self, node: NodeExprAssignment, manager) -> str:
        l_value = self.visit_expression(node.l_value)
        r_value = self.visit_expression(node.r_value)
        return f"{{{l_value} = {r_value}}}"

    def visit_expr_group(self, node: NodeExprGroup, manager) -> str:
        return f"({self.visit_expression(node.expression)})"

    def visit_expr_binary(self, node: NodeExprBinary, manager) -> str:
        lhs = self.visit_expression(node.lhs)
        rhs = self.visit_expression(node.rhs)
        return f"({lhs} {BINARY_OPERATOR[node.operator]} {rhs})"

    def visit_expr_unary(self, node: NodeExprUnary, manager) -> str:
        expr = self.visit_expression(node.expression)
        return f"({UNARY_OPERATOR[node.operator]}{expr})"

    def visit_expr_call(self, node: NodeExprCall, manager) -> str:
        callee = self.visit_expression(node.callee)
        arguments = ','.join(self.visit_expression(argument) for argument in node.arguments)
        return f"{callee}({arguments})"

    def visit_expr_literal(self, node: NodeExprLiteral, manager) -> str:
        return str(node.value)

    def visit_expr_variable(self, node: NodeExprVariable, manager) -> str:
        name = self._get_node_name(node)
        return f"[Variable:({name})]"

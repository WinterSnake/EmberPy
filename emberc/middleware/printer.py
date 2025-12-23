##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Visitor: Printer              ##
##-------------------------------##

## Imports
from typing import cast
from .nodes import (
    NodeType,
    NodeTypeBuiltin, NodeTypeIdentifier,
    NodeDeclUnit, NodeDeclFunction, NodeDeclVariable,
    NodeStmtBlock, NodeStmtConditional, NodeStmtLoop,
    NodeStmtReturn, NodeStmtExpression,
    NodeExprAssignment, NodeExprGroup, NodeExprBinary, NodeExprUnary,
    NodeExprCall, NodeExprVariable, NodeExprLiteral,
)
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
    Node Visitor : Printer

    A pretty printer for all AST nodes
    """

    # -Constructor
    def __init__(self) -> None:
        super().__init__(self, self, self, self)
        self.indent: int = 0

    # -Instance Methods
    def _indent(self) -> str:
        return ' ' * self.indent

    def visit_type_builtin(self, node: NodeTypeBuiltin, manager) -> str:
        return f"[Builtin:{node.type.name}]"

    def visit_type_custom(self, node: NodeTypeIdentifier, manager) -> str:
        return f"[Custom:{node.id}]"

    def visit_decl_unit(self, node: NodeDeclUnit, manager) -> str:
        lines = []
        for decl in node.body:
            lines.append(self.visit(decl))
        return '\n'.join(lines)

    def visit_decl_function(self, node: NodeDeclFunction, manager) -> str:
        header = f"{self._indent()}{node.name}("
        parameters = ','.join(self.visit_declaration(parameter) for parameter in node.parameters)
        ret = self.visit_type(cast(NodeType, node.type))
        body = self.visit_statement(node.body)
        return f"{header}{parameters}):{ret}\n{body}"

    def visit_decl_variable(self, node: NodeDeclVariable, manager) -> str:
        _type = self.visit_type(cast(NodeType, node.type))
        decl = f"{self._indent()}{{{_type}{node.name}"
        if node.has_initializer:
            decl += f" = {self.visit_expression(node.initializer)}"
        return decl + '}'

    def visit_stmt_block(self, node: NodeStmtBlock, manager) -> str:
        header = f"{self._indent()}{{"
        self.indent += 1
        body = '\n'.join(self.visit(elem) for elem in node.body)
        self.indent -= 1
        footer = f"{self._indent()}}}"
        return f"{header}\n{body}\n{footer}"

    def visit_stmt_conditional(self, node: NodeStmtConditional, manager) -> str:
        cond = self.visit_expression(node.condition)
        body = self.visit_statement(node.then_branch)
        block = f"{self._indent()}if({cond})\n{body}\n"
        if node.has_else_branch:
            else_body = self.visit_statement(node.else_branch)
            block += f"{self._indent()}else\n{else_body}"
        return block

    def visit_stmt_loop(self, node: NodeStmtLoop, manager) -> str:
        cond = self.visit_expression(node.condition)
        body = self.visit_statement(node.body)
        return f"{self._indent()}while({cond})\n{body}"

    def visit_stmt_return(self, node: NodeStmtReturn, manager) -> str:
        header = f"{self._indent()}ret["
        if node.has_value:
            return header + f"{self.visit_expression(node.value)}]"
        return header + "void]"

    def visit_stmt_expression(self, node: NodeStmtExpression, manager) -> str:
        return self._indent() + self.visit_expression(node.expression)

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
        return f"[Variable:({node.name})]"


## Body
printer = NodePrinter()

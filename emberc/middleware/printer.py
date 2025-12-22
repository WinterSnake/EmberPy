##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Visitor: Printer              ##
##-------------------------------##

## Imports
from .nodes import NodeDeclUnit, NodeExprBinary, NodeExprUnary, NodeExprLiteral
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

    def run(self, ast: NodeDeclUnit) -> None:
        print(self.visit_declaration(ast))

    def visit_type_builtin(self, node, manager) -> str:
        return f"[Builtin:{node.type.name}]"

    def visit_type_custom(self, node, manager) -> str:
        return f"[Custom:{node.id}]"

    def visit_decl_unit(self, node, manager) -> str:
        lines = []
        for decl in node.body:
            lines.append(self.visit(decl))
        return '\n'.join(lines)

    def visit_decl_variable(self, node, manager) -> str:
        _type = self.visit_type(node.type)
        decl = f"{self._indent()}{{{_type}{node.id}"
        if node.has_initializer:
            decl += f" = {self.visit_expression(node.initializer)}"
        return decl + '}'

    def visit_stmt_block(self, node, manager) -> str:
        header = f"{self._indent()}{{"
        self.indent += 1
        body = '\n'.join(self.visit(elem) for elem in node.body)
        self.indent -= 1
        footer = f"{self._indent()}}}"
        return f"{header}\n{body}\n{footer}"

    def visit_stmt_conditional(self, node, manager) -> str:
        cond = self.visit_expression(node.condition)
        body = self.visit_statement(node.body)
        block = f"{self._indent()}if({cond})\n{body}\n"
        if node.has_else_body:
            else_body = self.visit_statement(node.else_body)
            block += f"{self._indent()}else\n{else_body}"
        return block

    def visit_stmt_loop(self, node, manager) -> str:
        cond = self.visit_expression(node.condition)
        body = self.visit_statement(node.body)
        return f"{self._indent()}while({cond})\n{body}"

    def visit_stmt_expression(self, node, manager) -> str:
        return self._indent() + self.visit_expression(node.expression)

    def visit_expr_assignment(self, node, manager) -> str:
        l_value = self.visit_expression(node.l_value)
        r_value = self.visit_expression(node.r_value)
        return f"{{{l_value} = {r_value}}}"

    def visit_expr_group(self, node, manager) -> str:
        return f"({self.visit_expression(node.expression)})"

    def visit_expr_binary(self, node, manager) -> str:
        lhs = self.visit_expression(node.lhs)
        rhs = self.visit_expression(node.rhs)
        return f"({lhs} {BINARY_OPERATOR[node.operator]} {rhs})"

    def visit_expr_unary(self, node, manager) -> str:
        expr = self.visit_expression(node.expression)
        return f"({UNARY_OPERATOR[node.operator]}{expr})"

    def visit_expr_literal(self, node, manager) -> str:
        return str(node.value)

    def visit_expr_variable(self, node, manager) -> str:
        return f"[Variable:({node.id})]"


## Body
printer = NodePrinter()

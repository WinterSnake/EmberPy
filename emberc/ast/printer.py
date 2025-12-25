##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## AST: Printer                  ##
##-------------------------------##

## Imports
from .unresolved import (
    UnresolvedNode, UnresolvedUnitNode,
    UnresolvedTypeNode, UnresolvedDeclNode, UnresolvedStmtNode,
    UnresolvedDeclFunctionNode, UnresolvedDeclVariableNode,
    UnresolvedStmtBlockNode, UnresolvedStmtExpressionNode,
    UnresolvedStmtConditionalNode, UnresolvedStmtLoopWhileNode,
    UnresolvedStmtLoopDoNode, UnresolvedStmtLoopForNode,
    UnresolvedStmtReturnNode, UnresolvedStmtEmptyNode,
    UnresolvedGroupNode, UnresolvedExprEmptyNode,
    UnresolvedAssignNode, UnresolvedBinaryNode,
    UnresolvedUnaryPrefixNode, UnresolvedUnaryPostfixNode,
    UnresolvedIdentifierNode, UnresolvedLiteralNode, UnresolvedArrayNode,
    UnresolvedNodeVisitor,
)

## Constants
__all__ = ("unresolved_printer",)
UNARY_PREFIX_OPERATORS = {
    UnresolvedUnaryPrefixNode.Operator.Negative: '-',
    UnresolvedUnaryPrefixNode.Operator.LogNeg: '!',
    UnresolvedUnaryPrefixNode.Operator.BitNeg: '~',
    UnresolvedUnaryPrefixNode.Operator.Ptr: '*',
    UnresolvedUnaryPrefixNode.Operator.Ref: '^',
    UnresolvedUnaryPrefixNode.Operator.Deref: '@',
    UnresolvedUnaryPrefixNode.Operator.Slice: '[]',
    UnresolvedUnaryPrefixNode.Operator.SlicePtr: '[*]',
}
BINARY_OPERATORS = {
    UnresolvedBinaryNode.Operator.Range: '..',
    UnresolvedBinaryNode.Operator.Add: '+',
    UnresolvedBinaryNode.Operator.Sub: '-',
    UnresolvedBinaryNode.Operator.Mul: '*',
    UnresolvedBinaryNode.Operator.Div: '/',
    UnresolvedBinaryNode.Operator.Mod: '%',
    UnresolvedBinaryNode.Operator.BitXor: '^',
    UnresolvedBinaryNode.Operator.BitAnd: '&',
    UnresolvedBinaryNode.Operator.BitOr: '|',
    UnresolvedBinaryNode.Operator.ShiftL: '<<',
    UnresolvedBinaryNode.Operator.ShiftR: '>>',
    UnresolvedBinaryNode.Operator.LogAnd: '&&',
    UnresolvedBinaryNode.Operator.LogOr: '||',
    UnresolvedBinaryNode.Operator.Eq: '==',
    UnresolvedBinaryNode.Operator.NtEq: '!=',
    UnresolvedBinaryNode.Operator.Lt: '<',
    UnresolvedBinaryNode.Operator.Gt: '>',
    UnresolvedBinaryNode.Operator.LtEq: '<=',
    UnresolvedBinaryNode.Operator.GtEq: '>=',
}
ASSIGN_OPERATORS = {
    UnresolvedAssignNode.Operator.Eq: '=',
    UnresolvedAssignNode.Operator.AddEq: '+=',
    UnresolvedAssignNode.Operator.SubEq: '-=',
    UnresolvedAssignNode.Operator.MulEq: '*=',
    UnresolvedAssignNode.Operator.DivEq: '/=',
    UnresolvedAssignNode.Operator.ModEq: '%=',
    UnresolvedAssignNode.Operator.BitNegEq: '~=',
    UnresolvedAssignNode.Operator.BitXorEq: '^=',
    UnresolvedAssignNode.Operator.BitAndEq: '&=',
    UnresolvedAssignNode.Operator.BitOrEq: '|=',
    UnresolvedAssignNode.Operator.ShiftLEq: '<<=',
    UnresolvedAssignNode.Operator.ShiftREq: '>>=',
}


## Classes
class UnresolvedNodePrinter(UnresolvedNodeVisitor):
    """
    """

    # -Constructor
    def __init__(self) -> None:
        self._indent_level: int = 0

    # -Instance Methods
    def _get_indent(self) -> str:
        return ' ' * self._indent_level

    def run(self, node: UnresolvedUnitNode) -> str:
        return '\n'.join(self.visit(elem) for elem in node.children)

    def visit_type(self, node: UnresolvedTypeNode) -> str:
        return f"[Builtin:{node.type.name}]"

    def visit_decl_function(self, node: UnresolvedDeclFunctionNode) -> str:
        header = f"{self._get_indent()}fn ("
        for i, parameter in enumerate(node.parameters):
            header += f"{self.visit(parameter.type)} {parameter.name}"
            if parameter.has_initializer:
                header += f" = {self.visit(parameter.initializer)}"
            if i < node.arity - 1:
                header += ','
        header += f"):{self.visit(node.type)}\n"
        return header + self.visit(node.body)

    def visit_decl_variable(self, node: UnresolvedDeclVariableNode) -> str:
        decl = f"{self._get_indent()}{self.visit(node.type)}["
        for i, entry in enumerate(node.entries):
            decl += entry.name
            if entry.has_initializer:
                decl += f"={self.visit(entry.initializer)}"
            if i < len(node.entries) - 1:
                decl += ','
        return decl + ']'

    def visit_stmt_empty(self, node: UnresolvedStmtEmptyNode) -> str:
        return ""

    def visit_stmt_block(self, node: UnresolvedStmtBlockNode) -> str:
        header = f"{self._get_indent()}{{\n"
        self._indent_level += 1
        body = '\n'.join(
            f"{self._get_indent()}{self.visit(elem)}"
            for elem in node.body
        )
        self._indent_level -= 1
        return f"{header}{body}\n}}"

    def visit_stmt_condition(self, node: UnresolvedStmtConditionalNode) -> str:
        condition = self.visit(node.condition)
        header = f"{self._get_indent()}if ({condition})\n"
        header += self.visit(node.if_branch) + '\n'
        if node.has_else_branch:
            header += f"{self._get_indent()}else "
            header += self.visit(node.else_branch)
        return header

    def visit_stmt_loop_while(self, node: UnresolvedStmtLoopWhileNode) -> str:
        header = f"{self._get_indent()}while({self.visit(node.condition)})\n"
        return header + self.visit(node.body)

    def visit_stmt_loop_do(self, node: UnresolvedStmtLoopDoNode) -> str:
        header = f"{self._get_indent()}do\n"
        header += self.visit(node.body)
        header += f"while({self.visit(node.condition)})"
        return header

    def visit_stmt_loop_for(self, node: UnresolvedStmtLoopForNode) -> str:
        header = f"{self._get_indent()}for("
        if node.has_initializer:
            header += self.visit(node.initializer)
        header += ';'
        header += self.visit(node.condition) + ';'
        if node.has_increment:
            header += self.visit(node.increment)
        header += ")\n"
        return header + self.visit(node.body)

    def visit_stmt_return(self, node: UnresolvedStmtReturnNode) -> str:
        header = f"{self._get_indent()}return"
        if node.has_value:
            return header + self.visit(node.value)
        return header

    def visit_stmt_expression(self, node: UnresolvedStmtExpressionNode) -> str:
        return f"{self._get_indent()}{self.visit(node.expression)}"

    def visit_expr_empty(self, node: UnresolvedExprEmptyNode) -> str:
        return ""

    def visit_assignment(self, node: UnresolvedAssignNode) -> str:
        l_value = self.visit(node.l_value)
        operator = ASSIGN_OPERATORS[node.operator]
        r_value = self.visit(node.r_value)
        return f"{{{l_value} {operator} {r_value}}}"

    def visit_binary(self, node: UnresolvedBinaryNode) -> str:
        lhs = self.visit(node.lhs)
        operator = BINARY_OPERATORS[node.operator]
        rhs = self.visit(node.rhs)
        return f"({lhs} {operator} {rhs})"

    def visit_unary_prefix(self, node: UnresolvedUnaryPrefixNode) -> str:
        expr = self.visit(node.operand)
        operator = UNARY_PREFIX_OPERATORS[node.operator]
        return f"({operator}{expr})"

    def visit_unary_postfix(self, node: UnresolvedUnaryPostfixNode) -> str:
        head = self.visit(node.head)
        arguments = ','.join(self.visit(argument) for argument in node.arguments)
        match node.kind:
            case UnresolvedUnaryPostfixNode.Kind.Call:
                return f"{head}({arguments})"
            case UnresolvedUnaryPostfixNode.Kind.Subscript:
                return f"{head}[{arguments}]"

    def visit_group(self, node: UnresolvedGroupNode) -> str:
        expr = f"({self.visit(node.inner)})"
        if node.has_target:
            expr = f"({expr}; target={self.visit(node.target)})"
        return expr

    def visit_array(self, node: UnresolvedArrayNode) -> str:
        return '[' + ','.join(self.visit(elem) for elem in node.values) + ']'

    def visit_literal(self, node: UnresolvedLiteralNode) -> str:
        return str(node.value)

    def visit_identifier(self, node: UnresolvedIdentifierNode) -> str:
        return f"[Ident:{node.name}]"


## Body
unresolved_printer = UnresolvedNodePrinter()

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
    NodeStmtBlock, NodeStmtCondition, NodeStmtLoop, NodeStmtExpression,
    NodeExprAssignment, NodeExprBinary, NodeExprUnary,
    NodeExprGroup, NodeExprVariable, NodeExprLiteral,
)

## Classes
class PrinterWalker:
    """
    Printer Walker

    Walks through the AST tree and prints expressions with associativity
    """

    # -Instance Methods
    def visit_declaration_module(self, node: NodeDeclModule) -> None:
        for child in node.body:
            child.accept(self)

    def visit_declaration_function(self, node: NodeDeclFunction) -> None:
        for child in node.body:
            child.accept(self)

    def visit_declaration_variable(self, node: NodeDeclVariable) -> None:
        value = "None"
        if node.has_initializer:
            value = node.initializer.accept(self)
        print(f"{{Id({node.id}) = {value}}}")

    def visit_statement_block(self, node: NodeStmtBlock) -> None:
        for child in node.body:
            child.accept(self)

    def visit_statement_condition(self, node: NodeStmtCondition) -> None:
        node.body.accept(self)

    def visit_statement_loop(self, node: NodeStmtLoop) -> None:
        node.body.accept(self)

    def visit_statement_expression(self, node: NodeStmtExpression) -> None:
        value = node.expression.accept(self)
        print(value)

    def visit_expression_assignment(self, node: NodeExprAssignment) -> str:
        assert isinstance(node.l_value, NodeExprVariable)
        value = node.r_value.accept(self)
        return f"(Id({node.l_value.id}) = {value})"

    def visit_expression_binary(self, node: NodeExprBinary) -> str:
        lhs = node.lhs.accept(self)
        rhs = node.rhs.accept(self)
        operator: str
        match node.operator:
            case NodeExprBinary.Operator.Add:
                operator = '+'
            case NodeExprBinary.Operator.Sub:
                operator = '-'
            case NodeExprBinary.Operator.Mul:
                operator = '*'
            case NodeExprBinary.Operator.Div:
                operator = '/'
            case NodeExprBinary.Operator.Mod:
                operator = '%'
            case NodeExprBinary.Operator.Lt:
                operator = '<'
            case NodeExprBinary.Operator.Gt:
                operator = '>'
            case NodeExprBinary.Operator.LtEq:
                operator = "<="
            case NodeExprBinary.Operator.GtEq:
                operator = ">="
            case NodeExprBinary.Operator.EqEq:
                operator = "=="
            case NodeExprBinary.Operator.NtEq:
                operator = "!="
        return f"({lhs} {operator} {rhs})"

    def visit_expression_unary(self, node: NodeExprUnary) -> str:
        expression = node.expression.accept(self)
        match node.operator:
            case NodeExprUnary.Operator.Minus:
                return f"(-{expression})"

    def visit_expression_group(self, node: NodeExprGroup) -> str:
        return f"({node.expression.accept(self)})"

    def visit_expression_variable(self, node: NodeExprVariable) -> str:
        return f"Id({node.id})"

    def visit_expression_literal(self, node: NodeExprLiteral) -> str:
        return str(node.value)

    # -Static Methods
    @staticmethod
    def run(node: Node) -> None:
        visitor = PrinterWalker()
        node.accept(visitor)

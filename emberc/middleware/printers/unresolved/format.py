##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Printer: Formatted ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING, assert_never
from ....ast import (
    UnresolvedTypeNode,
    UnresolvedAssignNode,
    UnresolvedBinaryNode,
)

if TYPE_CHECKING:
    from ....ast import (
        UnresolvedNode,
        UnresolvedUnitNode,
        UnresolvedVariableNode,
        UnresolvedExprNode,
        UnresolvedGroupNode,
        UnresolvedLiteralNode,
        UnresolvedIdentifierNode,
    )

## Classes
class UnresolvedNodeFormatPrinter:
    """
    A visitor implementation for pretty-printing unresolved AST nodes as formatted text.

    Traverses the tree to generate a clean, human-readable string representation of the source 
    syntax, handling precedence grouping and standard code spacing.

    Provides a static `run` method to format and print the entire tree starting from a root node.
    """

    # -Instance Methods
    # --Types--
    def visit_type(self, node: UnresolvedTypeNode) -> str:
        match node.kind:
            case UnresolvedTypeNode.Kind.Int32:
                return 'int32'
            case _:
                assert_never(node.kind)

    # --Declarations--
    def visit_unit(self, node: UnresolvedUnitNode) -> str:
        output = (child.accept(self) for child in node)
        return '\n'.join(node for node in output if node)

    def visit_variable(self, node: UnresolvedVariableNode) -> str:
        # -Internal Methods
        def _visit_entry(entry: UnresolvedVariableNode.Entry) -> str:
            output = entry.name
            if entry.has_initializer:
                initializer = entry.initializer.accept(self)
                output += f"={initializer}"
            return output
        # -Body
        _type = node.type.accept(self)
        entries = (_visit_entry(entry) for entry in node)
        return _type + '[' + ','.join(entries) + ']'

    # --Statements--
    def visit_expression(self, node: UnresolvedExprNode) -> str:
        if node.has_expression:
            return node.expression.accept(self)
        return ''

    # --Expressions--
    def visit_group(self, node: UnresolvedGroupNode) -> str:
        return f"( {node.inner.accept(self)} )"

    def visit_assignment(self, node: UnresolvedAssignNode) -> str:
        operator: str
        l_value = node.l_value.accept(self)
        r_value = node.r_value.accept(self)
        match node.operator:
            case UnresolvedAssignNode.Operator.Eq:
                operator = '='
            case _:
                assert_never(node.operator)
        return f"({l_value} {operator} {r_value})"

    def visit_binary(self, node: UnresolvedBinaryNode) -> str:
        operator: str
        lhs = node.lhs.accept(self)
        rhs = node.rhs.accept(self)
        match node.operator:
            case UnresolvedBinaryNode.Operator.Add:
                operator = '+'
            case UnresolvedBinaryNode.Operator.Sub:
                operator = '-'
            case UnresolvedBinaryNode.Operator.Mul:
                operator = '*'
            case UnresolvedBinaryNode.Operator.Div:
                operator = '/'
            case UnresolvedBinaryNode.Operator.Mod:
                operator = '%'
            case _:
                assert_never(node.operator)
        return f"({lhs} {operator} {rhs})"

    def visit_literal(self, node: UnresolvedLiteralNode) -> str:
        return str(node.value)

    def visit_identifier(self, node: UnresolvedIdentifierNode) -> str:
        output = node.name
        if node.has_id:
            output += f"<id:{node.id}>"
        return output

    # -Static Methods
    @staticmethod
    def run(ast: UnresolvedNode) -> None:
        printer = UnresolvedNodeFormatPrinter()
        print(ast.accept(printer))

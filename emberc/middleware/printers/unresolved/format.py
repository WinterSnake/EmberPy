##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Printer: Formatted ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....ast import (
        UnresolvedNode,
        UnresolvedTypeNode,
        UnresolvedUnitNode,
        UnresolvedVariableNode,
        UnresolvedExprNode,
        UnresolvedGroupNode,
        UnresolvedAssignNode,
        UnresolvedBinaryNode,
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
        return str(node)

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
        return node.inner.accept(self)

    def visit_assignment(self, node: UnresolvedAssignNode) -> str:
        l_value = node.l_value.accept(self)
        r_value = node.r_value.accept(self)
        return f"({l_value} {str(node.operator)} {r_value})"

    def visit_binary(self, node: UnresolvedBinaryNode) -> str:
        lhs = node.lhs.accept(self)
        rhs = node.rhs.accept(self)
        return f"({lhs} {str(node.operator)} {rhs})"

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

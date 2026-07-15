##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Printer: Debug     ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING
from ....ast import (
    UnresolvedLiteralNode,
)

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
        UnresolvedIdentifierNode,
    )

## Classes
class UnresolvedNodeDebugPrinter:
    """
    A visitor implementation for generating detailed structural information 
    about unresolved AST nodes.

    Provides a static `run` method to output the debug info starting from a root node.
    """

    # -Constructor
    def __init__(self) -> None:
        self.depth: int = 0

    # -Instance Methods
    # --Types--
    def visit_type(self, node: UnresolvedTypeNode) -> str:
        return str(node)

    # --Declarations--
    def visit_unit(self, node: UnresolvedUnitNode) -> str:
        return ''

    def visit_variable(self, node: UnresolvedVariableNode) -> str:
        # -Internal Methods
        def _visit_entry(entry: UnresolvedVariableNode.Entry) -> str:
            return ''
        # -Body
        return ''

    # --Statements--
    def visit_expression(self, node: UnresolvedExprNode) -> str:
        if node.has_expression:
            self.depth += 1
            expr = node.expression.accept(self)
            print(expr)
            self.depth -= 1
        return ''

    # --Expressions--
    def visit_group(self, node: UnresolvedGroupNode) -> str:
        return ''

    def visit_assignment(self, node: UnresolvedAssignNode) -> str:
        return ''

    def visit_binary(self, node: UnresolvedBinaryNode) -> str:
        return ''

    def visit_literal(self, node: UnresolvedLiteralNode) -> str:
        return str(node.value)

    def visit_identifier(self, node: UnresolvedIdentifierNode) -> str:
        return ''

    # -Instance Methods: Helpers
    def get_indent(self) -> str:
        return ' ' * self.depth

    # -Static Methods
    @staticmethod
    def run(ast: UnresolvedNode) -> None:
        printer = UnresolvedNodeDebugPrinter()
        print(ast.accept(printer))

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Printer: Debug     ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING, assert_never
from ....ast import (
    UnresolvedTypeNode,
    UnresolvedAssignNode,
    UnresolvedBinaryNode,
    UnresolvedLiteralNode,
)

if TYPE_CHECKING:
    from ....diagnostics import SourceMap
    from ....ast import (
        UnresolvedNode,
        UnresolvedUnitNode,
        UnresolvedVariableNode,
        UnresolvedExprNode,
        UnresolvedGroupNode,
        UnresolvedIdentifierNode,
    )

## Classes
class UnresolvedNodeDebugPrinter:
    """
    A visitor implementation for generating detailed structural information 
    about unresolved AST nodes.

    Provides a static `run` method to output the debug info starting from a root node.
    """

    # -Instance Methods
    # --Types--
    def visit_type(self, node: UnresolvedTypeNode) -> str:
        return ''

    # --Declarations--
    def visit_unit(self, node: UnresolvedUnitNode) -> str:
        return ''

    def visit_variable(self, node: UnresolvedVariableNode) -> str:
        return ''

    # --Statements--
    def visit_expression(self, node: UnresolvedExprNode) -> str:
        return ''

    # --Expressions--
    def visit_group(self, node: UnresolvedGroupNode) -> str:
        return ''

    def visit_assignment(self, node: UnresolvedAssignNode) -> str:
        return ''

    def visit_binary(self, node: UnresolvedBinaryNode) -> str:
        return ''

    def visit_literal(self, node: UnresolvedLiteralNode) -> str:
        return ''

    def visit_identifier(self, node: UnresolvedIdentifierNode) -> str:
        return ''

    # -Instance Methods: Helpers
    def _visit_variable_entry(self, entry: UnresolvedVariableNode.Entry) -> str:
        return ''

    # -Static Methods
    @staticmethod
    def run(ast: UnresolvedNode) -> None:
        printer = UnresolvedNodeDebugPrinter()
        print(ast.accept(printer))

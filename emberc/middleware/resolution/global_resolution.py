##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolution: Global Resolution ##
##-------------------------------##

## Imports
from ..symbol_table import SymbolTable
from ...ast import (
    # -Unresolved
    UnresolvedUnitNode,
    UnresolvedDeclFunctionNode, UnresolvedDeclVariableNode,
    UnresolvedGroupNode,
    UnresolvedAssignNode, UnresolvedBinaryNode,
    UnresolvedUnaryPrefixNode, UnresolvedUnaryPostfixNode,
    UnresolvedIdentifierNode, UnresolvedLiteralNode, UnresolvedArrayNode,
    UnresolvedNodeVisitor, UnresolvedDefaultVisitorMixin,
    # -Resolved
    NodeType,
)


## Classes
class GlobalResolutionVisitor(
    UnresolvedDefaultVisitorMixin[None],
    UnresolvedNodeVisitor[UnresolvedUnitNode | None]
):
    """
    Global Resolution

    Iterates over global functions and variables and wires their
    type information and initializers
    """

    # -Constructor
    def __init__(self, symbol_table: SymbolTable) -> None:
        self._symbol_table = symbol_table

    # -Instance Methods
    def run(self, ast: UnresolvedUnitNode) -> UnresolvedUnitNode:
        for child in ast.children:
            self.visit(child)
        return ast

    def visit_decl_function(self, node: UnresolvedDeclFunctionNode) -> None:
        symbol = self._symbol_table.get(node.id)
        symbol.type.bind(self)

    def visit_decl_variable(self, node: UnresolvedDeclVariableNode) -> None:
        for entry in node.entries:
            symbol = self._symbol_table.get(entry.id)
            symbol.type.bind(self)
            if entry.has_initializer:
                self.visit(entry.initializer)

    def visit_assignment(self, node: UnresolvedAssignNode) -> None:
        self.visit(node.l_value)
        self.visit(node.r_value)

    def visit_binary(self, node: UnresolvedBinaryNode) -> None:
        self.visit(node.lhs)
        self.visit(node.rhs)

    def visit_unary_prefix(self, node: UnresolvedUnaryPrefixNode) -> None:
        self.visit(node.operand)

    def visit_unary_postfix(self, node: UnresolvedUnaryPostfixNode) -> None:
        self.visit(node.head)

    def visit_group(self, node: UnresolvedGroupNode) -> None:
        self.visit(node.inner)
        if node.has_target:
            self.visit(node.target)

    def visit_array(self, node: UnresolvedArrayNode) -> None:
        for value in node.values:
            self.visit(value)

    def visit_identifier(self, node: UnresolvedIdentifierNode) -> None:
        _id = self._symbol_table.find(node.name)
        assert _id is not None, "TODO: Error handling"
        node.id = _id

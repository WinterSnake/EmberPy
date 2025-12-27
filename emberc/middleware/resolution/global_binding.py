##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolution: Global Binding    ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import TYPE_CHECKING
from .type_factory import TypeFactoryVisitor
from ...ast import (
    UnresolvedUnitNode, UnresolvedNodeVisitor, UnresolvedDefaultVisitorMixin
)

if TYPE_CHECKING:
    from ..symbol_table import SymbolTable
    from ...ast import (
        UnresolvedDeclFunctionNode, UnresolvedDeclVariableNode, NodeType,
    )


## Classes
class GlobalBindingVisitor(
    UnresolvedDefaultVisitorMixin[None],
    UnresolvedNodeVisitor[None]
):
    """
    Global Binding

    Traverses the AST tree and binds globals (variables and functions)
    by their type and name to the symbol table at the root scope
    """

    # -Constructor
    def __init__(self, symbol_table: SymbolTable) -> None:
        self._symbol_table = symbol_table
        self._type_factory = TypeFactoryVisitor(symbol_table)

    # -Instance Methods
    def run(self, ast: UnresolvedUnitNode) -> None:
        for child in ast.children:
            self.visit(child)

    def visit_decl_function(self, node: UnresolvedDeclFunctionNode) -> None:
        _type = self._type_factory.visit(node.type)
        assert _type is not None, "TODO: Error handling"
        parameter_types: list[NodeType] = []
        for parameter in node.parameters:
            parameter_type = self._type_factory.visit(parameter.type)
            assert parameter_type is not None, "TODO: Error handling"
            parameter_types.append(parameter_type)
        _id = self._symbol_table.add_function(node.name, _type, parameter_types)
        assert _id is not None, "TODO: Error handling"
        node.id = _id

    def visit_decl_variable(self, node: UnresolvedDeclVariableNode) -> None:
        _type = self._type_factory.visit(node.type)
        assert _type is not None, "TODO: Error handling"
        for entry in node.entries:
            _id = self._symbol_table.add_variable(entry.name, _type)
            assert _id is not None, "TODO: Error handling"
            entry.id = _id

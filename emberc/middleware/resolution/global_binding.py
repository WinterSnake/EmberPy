##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolution: Global Binding    ##
##-------------------------------##

## Imports
from .type_factory import TypeFactoryVisitor
from ..symbol_table import SymbolTable
from ...ast import (
    # -Unresolved
    UnresolvedUnitNode,
    UnresolvedDeclFunctionNode, UnresolvedDeclVariableNode,
    UnresolvedNodeVisitor, UnresolvedDefaultVisitorMixin,
    # -Resolved
    NodeType,
)


## Classes
class GlobalBindingVisitor(
    UnresolvedDefaultVisitorMixin[None],
    UnresolvedNodeVisitor[UnresolvedUnitNode | None]
):
    """
    Global Binding

    Iterates over global functions and variables and registers their
    type information and name to the symbol table in root scope
    """

    # -Constructor
    def __init__(self, symbol_table: SymbolTable) -> None:
        self._symbol_table = symbol_table
        self._type_factory = TypeFactoryVisitor(symbol_table)

    # -Instance Methods
    def run(self, ast: UnresolvedUnitNode) -> UnresolvedUnitNode:
        for child in ast.children:
            self.visit(child)
        return ast

    def visit_decl_function(self, node: UnresolvedDeclFunctionNode) -> None:
        _type = self._type_factory.visit(node.type)
        assert _type is not None
        parameter_types: list[NodeType] = []
        for parameter in node.parameters:
            parameter_type = self._type_factory.visit(parameter.type)
            assert parameter_type is not None
            parameter_types.append(parameter_type)
        _id = self._symbol_table.add_function(node.name, _type, parameter_types)
        assert _id is not None
        node.id = _id

    def visit_decl_variable(self, node: UnresolvedDeclVariableNode) -> None:
        _type = self._type_factory.visit(node.type)
        assert _type is not None
        for entry in node.entries:
            _id = self._symbol_table.add_variable(entry.name, _type)
            assert _id is not None
            entry.id = _id

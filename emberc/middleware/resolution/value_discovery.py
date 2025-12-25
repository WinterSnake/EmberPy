##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolution: Value Discovery   ##
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
class GlobalValueDiscoveryVisitor(
    UnresolvedDefaultVisitorMixin[None],
    UnresolvedNodeVisitor[UnresolvedUnitNode | None]
):
    """
    Global Value Discovery

    Iterates over global functions and variables and registers heir type
    information with their name to the symbol table in root scope
    """

    # -Constructor
    def __init__(self, symbol_table: SymbolTable) -> None:
        self._symbol_table = symbol_table
        self._type_factory = TypeFactoryVisitor(symbol_table)

    # -Instance Methods
    def run(self, node: UnresolvedUnitNode) -> UnresolvedUnitNode:
        for child in node.children:
            self.visit(child)
        return node

    def visit_decl_function(self, node: UnresolvedDeclFunctionNode) -> None:
        _type = self._type_factory.visit(node.type)
        assert _type is not None
        parameters: list[NodeType] = []
        for parameter in node.parameters:
            param = self._type_factory.visit(parameter.type)
            assert param is not None
            parameters.append(param)
        _id = self._symbol_table.add_function(node.name, _type, parameters)
        assert _id is not None
        node.id = _id

    def visit_decl_variable(self, node: UnresolvedDeclVariableNode) -> None:
        _type = self._type_factory.visit(node.type)
        assert _type is not None
        for entry in node.entries:
            _id = self._symbol_table.add_variable(entry.name, _type)
            assert _id is not None
            entry.id = _id

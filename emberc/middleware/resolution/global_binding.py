##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolution Pass: Global Bind  ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING
from .type_builder import TypeBuilderFactory
from ...ast import (
    UnresolvedNodeVisitor,
    UnresolvedNullVisitorMixin,
)

if TYPE_CHECKING:
    from ..symbol_table import SymbolTable
    from ...ast import (
        UnresolvedUnitNode,
        UnresolvedFunctionNode,
        UnresolvedVariableNode,
    )


## Classes
class GlobalBindingWalker(
    UnresolvedNullVisitorMixin[None],
    UnresolvedNodeVisitor[None]
):
    """
    Global Binder

    Discovers and registers global-scope symbols. This includes: unit level functions,
    and unit level variables. It utilizes a type builder to resolve surface level types.
    """

    # -Constructor
    def __init__(self, symbol_table: SymbolTable) -> None:
        self._symbol_table: SymbolTable = symbol_table
        self._type_builder = TypeBuilderFactory(symbol_table)

    # -Instance Methods: Visitor
    def visit_unit(self, node: UnresolvedUnitNode) -> None:
        for _node in node.nodes:
            self.visit(_node)

    def visit_decl_function(self, node: UnresolvedFunctionNode) -> None:
        return_type = self._type_builder.run(node.return_type)
        parameter_types = [
            self._type_builder.run(parameter.type)
            for parameter in node.parameters
        ]
        node._id = self._symbol_table.add_function(
            node.name, return_type, parameter_types
        )
        assert node._id is not None, "TODO: Error handling"

    def visit_decl_variable(self, node: UnresolvedVariableNode) -> None:
        _type = self._type_builder.run(node.type)
        for entry in node.entries:
            entry._id = self._symbol_table.add_variable(entry.name, _type)
            assert entry._id is not None

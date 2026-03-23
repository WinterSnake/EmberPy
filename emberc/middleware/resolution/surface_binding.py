##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolution Pass: Global Bind  ##
##-------------------------------##

## Imports
from collections.abc import Collection
from typing import TYPE_CHECKING, cast
from .type_builder import TypeBuilderFactory
from ...ast import (
    # -Unresolved
    UnresolvedNodeVisitor,
    UnresolvedNullVisitorMixin,
    UnresolvedEnumNode,
)

if TYPE_CHECKING:
    from ..symbol_table import SymbolTable
    from ...ast import (
        UnresolvedUnitNode,
        UnresolvedFunctionNode,
        UnresolvedVariableNode,
    )


## Classes
class SurfaceBindingWalker(
    UnresolvedNullVisitorMixin[None],
    UnresolvedNodeVisitor[None]
):
    """
    Surface Binder [Pass 2]

    Maps the 'public' interface of all discovered types and global entities.
    Registers function signatures, global variables, struct fields, and 
    tagged enum variants into the symbol table.
    """

    # -Constructor
    def __init__(self, symbol_table: SymbolTable) -> None:
        self._symbol_table: SymbolTable = symbol_table
        self._type_builder = TypeBuilderFactory(symbol_table)

    # -Instance Methods: Visitor
    def visit_unit(self, node: UnresolvedUnitNode) -> None:
        for _node in node.nodes:
            self.visit(_node)

    def visit_decl_enum(self, node: UnresolvedEnumNode) -> None:
        if not node.is_tagged:
            return
        # -Entries
        for entry in node.entries:
            if not entry.has_value:
                continue
            # -Tags
            for tag in cast(Collection[UnresolvedEnumNode.Tag], entry.value):
                _type = self._type_builder.run(tag.type)
                tag._id = self._symbol_table.add_enum_variant(
                    entry.id, tag.name, _type
                )
                assert tag.has_id, "TODO: Error handling"

    def visit_decl_function(self, node: UnresolvedFunctionNode) -> None:
        return_type = self._type_builder.run(node.return_type)
        parameter_types = [
            self._type_builder.run(parameter.type)
            for parameter in node.parameters
        ]
        node._id = self._symbol_table.add_function(
            node.name, return_type, parameter_types
        )
        assert node.has_id, "TODO: Error handling"

    def visit_decl_variable(self, node: UnresolvedVariableNode) -> None:
        _type = self._type_builder.run(node.type)
        for entry in node.entries:
            entry._id = self._symbol_table.add_variable(entry.name, _type)
            assert entry.has_id, "TODO: Error handling"

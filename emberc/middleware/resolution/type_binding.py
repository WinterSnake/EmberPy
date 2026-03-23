##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolution Pass: Type Bind    ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING
from .type_builder import TypeBuilderFactory
from ...ast import (
    # -Unresolved
    UnresolvedNodeVisitor,
    UnresolvedNullVisitorMixin,
    UnresolvedEnumNode,
    # -Resolved
    TypeNode,
    PendingTypeNode,
    EnumTypeNode,
)

if TYPE_CHECKING:
    from ..symbol_table import SymbolTable
    from ...ast import (
        UnresolvedUnitNode,
    )


## Classes
class TypeBindingWalker(
    UnresolvedNullVisitorMixin[None],
    UnresolvedNodeVisitor[None]
):
    """
    Type Binder

    Discovers and registers typed symbols. This includes: struct and enum declarations.
    It utilizes a type builder to resolve surface level types.
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
        # -Node
        underlying: TypeNode = PendingTypeNode()
        if node.has_type:
            underlying = self._type_builder.run(node.type)
        _type = EnumTypeNode(underlying)
        node._id = self._symbol_table.add_enum(
            node.name, _type, node.is_tagged
        )
        assert node._id is not None, "TODO: Error handling"
        # -Entries
        for entry in node.entries:
            entry._id = self._symbol_table.add_enum_member(
                node.id, entry.name, node.is_tagged
            )
            assert entry._id is not None, "TODO: Error handling"

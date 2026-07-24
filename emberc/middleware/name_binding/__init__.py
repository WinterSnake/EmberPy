##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Middleware: Name Binding      ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING
from .local_binder import LocalNameBinder
from .type_factory import TypeFactory
from ..symbol_table import Symbol, SymbolTable

if TYPE_CHECKING:
    from collections.abc import Sequence
    from ...ast import UnresolvedNode
    from ...diagnostics import DiagnosticEngine

## Constants
__all__ = (
    "LocalNameBinder",
    "TypeFactory",
    "resolve_name_binding",
)


## Functions
def resolve_name_binding(
    unit: UnresolvedNode, engine: DiagnosticEngine,
) -> Sequence[Symbol]:
    """
    Name Binding Pass [Group]

    Traverses over an unresolved AST to bind identifiers to the symbol table.
    Additionally provides type information into the symbol meta-data.
    """
    symbol_table = SymbolTable()
    LocalNameBinder.run(unit, symbol_table, engine)
    return symbol_table.symbols

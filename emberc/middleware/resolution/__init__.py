##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolution Pass               ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING
from .global_binding import GlobalBindingWalker
from .type_binding import TypeBindingWalker

if TYPE_CHECKING:
    from ...ast import UnresolvedUnitNode
    from ..symbol_table import SymbolTable

## Constants
__all__ = (
    "GlobalBindingWalker",
    "TypeBindingWalker",
    "resolve_program_ast",
)


## Functions
def resolve_program_ast(
    symbol_table: SymbolTable, ast: UnresolvedUnitNode
) -> None:
    """
    Resolution Orchestrator

    Transforms a series of UnresolvedUnitNodes and returns a fully bound
    and typed semantic model. It executes the series of pipelines to go from
    an Unresolved tree to a fully resolved program.
    """
    type_binder = TypeBindingWalker(symbol_table)
    type_binder.visit(ast)
    global_binder = GlobalBindingWalker(symbol_table)
    global_binder.visit(ast)
    for symbol in symbol_table._symbols:
        print(symbol)

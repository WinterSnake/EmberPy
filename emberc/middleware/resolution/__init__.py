##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Middleware: Resolution Pass   ##
##-------------------------------##

## Imports
from .type_factory import TypeFactoryVisitor
from .value_discovery import GlobalValueDiscoveryVisitor
from ..symbol_table import SymbolTable
from ...ast import UnresolvedUnitNode

## Constants
__all__ = (
    "GlobalValueDiscoveryVisitor",
    "resolve_ast",
)


## Functions
def resolve_ast(
    ast: UnresolvedUnitNode, root: SymbolTable | None = None
) -> UnresolvedUnitNode:
    """Runs discovery and binding passes to produce a resolved AST tree"""
    table = SymbolTable(root)
    ast = GlobalValueDiscoveryVisitor(table).run(ast)
    return ast

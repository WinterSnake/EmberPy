##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Pass: Resolution              ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import TYPE_CHECKING
from .global_binding import GlobalBindingVisitor
from .local_binding import LocalBindingVisitor
from .type_factory import TypeFactoryVisitor
from .variable_evaluator import VariableEvaluatorVisitor
from ..symbol_table import SymbolTable

if TYPE_CHECKING:
    from ...ast import UnresolvedUnitNode

## Constants
__all__ = (
    "GlobalBindingVisitor", "LocalBindingVisitor",
    "TypeFactoryVisitor", "VariableEvaluatorVisitor",
    "resolve_ast"
)


## Functions
def resolve_ast(
    ast: UnresolvedUnitNode, root: SymbolTable | None = None
) -> UnresolvedUnitNode:
    """Runs binding passes and returns a lowered resolved AST"""
    table = SymbolTable(root)
    ast = GlobalBindingVisitor(table).run(ast)
    ast = LocalBindingVisitor(table).run(ast)
    return ast

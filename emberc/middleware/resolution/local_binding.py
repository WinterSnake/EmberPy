##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolution: Local Binding     ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING
from .type_factory import TypeFactory

if TYPE_CHECKING:
    from ..symbol_table import SymbolTable
    from ...ast import (
        UnresolvedNode,
        UnresolvedTypeNode,
        UnresolvedUnitNode,
        UnresolvedVariableNode,
        UnresolvedExprNode,
        UnresolvedGroupNode,
        UnresolvedAssignNode,
        UnresolvedBinaryNode,
        UnresolvedLiteralNode,
        UnresolvedIdentifierNode,
    )
    from ...diagnostics import DiagnosticEngine


## Classes
class LocalBinderPass:
    """
    Resolution Pass [1]
    
    An AST visitor that binds variable declarations and identifier usages to their 
    respective IDs in the symbol table, while flagging redeclarations and undeclared variables.
    """

    # -Constructor
    def __init__(
        self, symbol_table: SymbolTable, engine: DiagnosticEngine
    ) -> None:
        self._symbol_table = symbol_table
        self._engine = engine
        self._type_builder = TypeFactory(symbol_table, engine)

    # -Instance Methods
    # --Types--
    def visit_type(self, node: UnresolvedTypeNode) -> None:
        pass

    # --Declarations--
    def visit_unit(self, node: UnresolvedUnitNode) -> None:
        for child in node:
            child.accept(self)

    def visit_variable(self, node: UnresolvedVariableNode) -> None:
        _type = node.type.accept(self._type_builder)
        for entry in node:
            if entry.has_initializer:
                entry.initializer.accept(self)
            entry._id = self._symbol_table.add_variable(entry.name, _type)
            if entry._id is None:
                self._engine.error(f"Tried declaring already declared variable '{entry.name}'")

    # --Statements--
    def visit_expression(self, node: UnresolvedExprNode) -> None:
        if node.has_expression:
            node.expression.accept(self)

    # --Expressions--
    def visit_group(self, node: UnresolvedGroupNode) -> None:
        node.inner.accept(self)

    def visit_assignment(self, node: UnresolvedAssignNode) -> None:
        node.l_value.accept(self)
        node.r_value.accept(self)

    def visit_binary(self, node: UnresolvedBinaryNode) -> None:
        node.lhs.accept(self)
        node.rhs.accept(self)

    def visit_literal(self, node: UnresolvedLiteralNode) -> None:
        pass

    def visit_identifier(self, node: UnresolvedIdentifierNode) -> None:
        node._id = self._symbol_table.find_id(node.name)
        if node._id is None:
            self._engine.error(f"Tried using undeclared variable '{node.name}'")

    # -Static Methods
    @staticmethod
    def run(
        node: UnresolvedNode, symbol_table: SymbolTable, engine: DiagnosticEngine
    ) -> None:
        binder = LocalBinderPass(symbol_table, engine)
        node.accept(binder)

    # -Class Properties
    __slots__ = ("_symbol_table", "_engine", "_type_builder")

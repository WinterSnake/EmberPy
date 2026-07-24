##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Name Binding: Local           ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING
from .type_factory import TypeFactory
from ...ast import (
    UnresolvedNode,
    UnresolvedLiteralRouterMixin,
    UnresolvedSequenceRouterMixin,
)
from ...diagnostics import Diagnostic

if TYPE_CHECKING:
    from ..symbol_table import SymbolTable
    from ...ast import (
        UnresolvedTypeNode,
        UnresolvedSequenceNode,
        UnresolvedLiteralNode,
        UnresolvedVariableNode,
        UnresolvedBlockNode,
        UnresolvedConditionalNode,
        UnresolvedExpressionNode,
        UnresolvedGroupNode,
        UnresolvedAssignNode,
        UnresolvedBinaryNode,
        UnresolvedUnaryPrefixNode,
        UnresolvedIdentifierNode,
    )
    from ...diagnostics import DiagnosticEngine


## Classes
class LocalNameBinder(
    UnresolvedSequenceRouterMixin[None],
    UnresolvedLiteralRouterMixin[None]
):
    """
    Local Name Binding Pass [Order=0]

    Walks the entire AST tree to bind every internal identifier to a symbol.
    Creates and pops necessary scoping to allow variable shadowing while flagging
    redeclarations as well as use before declared names.
    """
    # -Constructor
    def __init__(
        self, symbol_table: SymbolTable,
        engine: DiagnosticEngine,
    ) -> None:
        self._engine = engine
        self._symbol_table = symbol_table
        self._type_factory = TypeFactory()

    # -Instance Methods
    # --Types--
    def visit_type(self, node: UnresolvedTypeNode) -> None:
        pass

    # --Declarations--
    def visit_variable(self, node: UnresolvedVariableNode) -> None:
        _type = node.type.accept(self._type_factory)
        for entry in node:
            if entry.has_initializer:
                entry.initializer.accept(self)
            entry._id = self._symbol_table.add_variable(entry.name, _type)
            if entry.has_id:
                continue
            self._engine.error(Diagnostic.Code.E3001, entry.location, entry.name)

    # --Statements--
    def visit_block(self, node: UnresolvedBlockNode) -> None:
        self._symbol_table.push()
        super().visit_block(node)
        _ = self._symbol_table.pop()

    def visit_conditional(self, node: UnresolvedConditionalNode) -> None:
        node.condition.accept(self)
        node.then_branch.accept(self)
        if node.has_else_branch:
            node.else_branch.accept(self)

    def visit_expression(self, node: UnresolvedExpressionNode) -> None:
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

    def visit_unary(self, node: UnresolvedUnaryPrefixNode) -> None:
        node.operand.accept(self)

    def visit_identifier(self, node: UnresolvedIdentifierNode) -> None:
        node._id = self._symbol_table.find_id(node.name)
        if node.has_id:
            return
        self._engine.error(Diagnostic.Code.E3002, node.location, node.name)

    # --Extensions--
    def visit_sequence(self, node: UnresolvedSequenceNode) -> None:
        for _node in node:
            _node.accept(self)

    def visit_literal(self, node: UnresolvedLiteralNode) -> None:
        pass

    # -Static Methods
    @staticmethod
    def run(
        node: UnresolvedNode,
        symbol_table: SymbolTable,
        engine: DiagnosticEngine,
    ) -> None:
        binder = LocalNameBinder(symbol_table, engine)
        node.accept(binder)

    # -Class Properties
    __slots__ = (
        "_engine",
        "_symbol_table",
        "_type_factory",
    )

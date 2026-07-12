##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Middleware: Resolution        ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING, NoReturn, assert_never, cast
from .local_binding import LocalBinderPass
from ..symbol_table import Symbol, SymbolTable
from ...ast import (
    # -Unresolved
    UnresolvedAssignNode,
    UnresolvedBinaryNode,
    UnresolvedLiteralNode,
    # -Resolved: Declarations
    DeclNode,
    DeclUnitNode,
    DeclSequenceNode,
    DeclVariableNode,
    # -Resolved: Statement
    StmtEmptyNode,
    StmtExpressionNode,
    # -Resolved: Expression
    ExprNode,
    ExprAssignNode,
    ExprBinaryNode,
    ExprIntegerNode,
    ExprVariableNode,
)

if TYPE_CHECKING:
    from collections.abc import Sequence
    from ...ast import (
        # -Unresolved
        UnresolvedNode,
        UnresolvedTypeNode,
        UnresolvedUnitNode,
        UnresolvedVariableNode,
        UnresolvedExprNode,
        UnresolvedGroupNode,
        UnresolvedIdentifierNode,
        # -Resolved
        ResolvedNode,
    )
    from ...diagnostics import DiagnosticEngine

## Constants
__all__ = ("resolve_ast",)


## Functions
def resolve_ast(
    unit: UnresolvedNode, engine: DiagnosticEngine
) -> tuple[Sequence[Symbol], ResolvedNode] | None:
    """
    Orchestrates the AST resolution pipeline.

    Binds local variables to a new symbol table and, if no diagnostic errors 
    are encountered, lowers the unresolved AST into its resolved equivalent.
    """
    # -TODO: symbol table parent root
    symbol_table = SymbolTable()
    LocalBinderPass.run(unit, symbol_table, engine)
    # -TODO: early break on errors
    if engine.has_error:
        return None
    resolved_ast = ResolveTransformer.run(unit, symbol_table)
    return (symbol_table.symbols, resolved_ast)


## Classes
class ResolveTransformer:
    """
    Resolution Pass [2]

    Lowers an unresolved AST into its strongly-typed, resolved equivalent by mapping
    identifiers to their respective symbols and eliminating structural syntax abstractions.
    """
    # -Constructor
    def __init__(self, symbol_table: SymbolTable) -> None:
        self._symbol_table = symbol_table

    # -Instance Methods
    # --Types--
    def visit_type(self, node: UnresolvedTypeNode) -> NoReturn:
        assert False, "Tried calling resolve transformer with a type node"

    # --Declarations--
    def visit_unit(self, node: UnresolvedUnitNode) -> ResolvedNode:
        nodes: list[DeclNode] = []
        for child in node:
            _child = child.accept(self)
            match _child:
                case StmtEmptyNode():
                    continue
                case DeclSequenceNode():
                    nodes.extend(_child)
                case _:
                    nodes.append(cast(DeclNode, _child))
        return DeclUnitNode(nodes)

    def visit_variable(self, node: UnresolvedVariableNode) -> ResolvedNode:
        entries: list[DeclNode] = []
        for entry in node:
            initializer: ExprNode | None = None
            if entry.has_initializer:
                initializer = cast(ExprNode, entry.initializer.accept(self))
            _entry = DeclVariableNode(entry.id, initializer)
            entries.append(_entry)
        return DeclSequenceNode(entries)

    # --Statements--
    def visit_expression(self, node: UnresolvedExprNode) -> ResolvedNode:
        if not node.has_expression:
            return StmtEmptyNode()
        expr = cast(ExprNode, node.expression.accept(self))
        return StmtExpressionNode(expr)

    # --Expressions--
    def visit_group(self, node: UnresolvedGroupNode) -> ResolvedNode:
        return node.inner.accept(self)

    def visit_assignment(self, node: UnresolvedAssignNode) -> ResolvedNode:
        l_value = cast(ExprNode, node.l_value.accept(self))
        r_value = cast(ExprNode, node.r_value.accept(self))
        return ExprAssignNode(node.operator, l_value, r_value)

    def visit_binary(self, node: UnresolvedBinaryNode) -> ResolvedNode:
        lhs = cast(ExprNode, node.lhs.accept(self))
        rhs = cast(ExprNode, node.rhs.accept(self))
        return ExprBinaryNode(node.operator, lhs, rhs)

    def visit_literal(self, node: UnresolvedLiteralNode) -> ResolvedNode:
        match node.kind:
            case UnresolvedLiteralNode.Kind.Integer:
                return ExprIntegerNode(node.value_as(int))
            case _:
                assert_never(node.kind)

    def visit_identifier(self, node: UnresolvedIdentifierNode) -> ResolvedNode:
        return ExprVariableNode.from_symbol(self._symbol_table[node.id])

    # -Static Methods
    @staticmethod
    def run(node: UnresolvedNode, symbol_table: SymbolTable) -> ResolvedNode:
        factory = ResolveTransformer(symbol_table)
        return node.accept(factory)

    # -Class Properties
    __slots__ = ("_symbol_table",)

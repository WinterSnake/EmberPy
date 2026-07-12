##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolution: Type Factory      ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING, NoReturn, assert_never
from ...ast import (
    # -Unresolved
    UnresolvedTypeNode,
    # -Resolved
    TypePrimitive,
)

if TYPE_CHECKING:
    from ..symbol_table import SymbolTable
    from ...ast import (
        # -Unresolved
        UnresolvedNode,
        UnresolvedUnitNode,
        UnresolvedVariableNode,
        UnresolvedExprNode,
        UnresolvedGroupNode,
        UnresolvedAssignNode,
        UnresolvedBinaryNode,
        UnresolvedLiteralNode,
        UnresolvedIdentifierNode,
        # -Resolved
        TypeNode,
    )
    from ...diagnostics import DiagnosticEngine


## Classes
class TypeFactory:
    """
    Lowers unresolved AST type subtrees into concrete TypeNodes.
    
    Implements a strict AST visitor pattern to dynamically map primitive
    types, type identifiers, and complex type constructs to their resolved type forms.
    """

    # -Constructor
    def __init__(
        self, symbol_table: SymbolTable, engine: DiagnosticEngine
    ) -> None:
        self._symbol_table = symbol_table
        self._engine = engine

    # -Instance Methods
    # --Types--
    def visit_type(self, node: UnresolvedTypeNode) -> TypeNode:
        match node.kind:
            case UnresolvedTypeNode.Kind.Int32:
                return TypePrimitive.int32
            case _:
                assert_never(node.kind)

    # --Declarations--
    def visit_unit(self, node: UnresolvedUnitNode) -> NoReturn:
        assert False, "Tried calling type factory with a unit node"

    def visit_variable(self, node: UnresolvedVariableNode) -> NoReturn:
        assert False, "Tried calling type factory with a variable node"

    # --Statements--
    def visit_expression(self, node: UnresolvedExprNode) -> NoReturn:
        assert False, "Tried calling type factory with an expression node"

    # --Expressions--
    def visit_group(self, node: UnresolvedGroupNode) -> NoReturn:
        assert False, "Tried calling type factory with a group node"

    def visit_assignment(self, node: UnresolvedAssignNode) -> NoReturn:
        assert False, "Tried calling type factory with an assignment node"

    def visit_binary(self, node: UnresolvedBinaryNode) -> NoReturn:
        assert False, "Tried calling type factory with a binary node"

    def visit_literal(self, node: UnresolvedLiteralNode) -> NoReturn:
        assert False, "Tried calling type factory with a literal node"

    def visit_identifier(self, node: UnresolvedIdentifierNode) -> NoReturn:
        assert False, "Tried calling type factory with an identifier node"

    # -Class Properties
    __slots__ = ("_symbol_table", "_engine")

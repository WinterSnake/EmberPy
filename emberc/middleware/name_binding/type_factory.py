##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Name Binding: Type Factory    ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING, NoReturn, assert_never
from ...ast import (
    # -Common
    PrimitiveType,
    # -Unresolved
    UnresolvedSequenceRouterMixin,
    UnresolvedLiteralRouterMixin,
    # -Resolved
    TypeNode,
    TypePrimitiveNode,
)

if TYPE_CHECKING:
    from ...ast import (
        UnresolvedTypeNode,
        UnresolvedSequenceNode,
        UnresolvedLiteralNode,
        UnresolvedVariableNode,
        UnresolvedConditionalNode,
        UnresolvedExpressionNode,
        UnresolvedGroupNode,
        UnresolvedAssignNode,
        UnresolvedBinaryNode,
        UnresolvedUnaryPrefixNode,
        UnresolvedIdentifierNode,
    )

## Classes
class TypeFactory(
    UnresolvedSequenceRouterMixin[TypeNode],
    UnresolvedLiteralRouterMixin[TypeNode],
):
    """
    Type Factory Builder

    A specialized AST visitor for creating and transforming
    unresolved nodes into resolved Type signature nodes.
    """
    # -Instance Methods
    # --Types--
    def visit_type(self, node: UnresolvedTypeNode) -> TypeNode:
        match node.kind:
            case PrimitiveType.Void:
                return TypePrimitiveNode.void
            case PrimitiveType.Boolean:
                return TypePrimitiveNode.boolean
            case PrimitiveType.Int8:
                return TypePrimitiveNode.int8
            case PrimitiveType.Int16:
                return TypePrimitiveNode.int16
            case PrimitiveType.Int32:
                return TypePrimitiveNode.int32
            case PrimitiveType.Int64:
                return TypePrimitiveNode.int64
            case PrimitiveType.UInt8:
                return TypePrimitiveNode.uint8
            case PrimitiveType.UInt16:
                return TypePrimitiveNode.uint16
            case PrimitiveType.UInt32:
                return TypePrimitiveNode.uint32
            case PrimitiveType.UInt64:
                return TypePrimitiveNode.uint64
            case PrimitiveType.ISize:
                return TypePrimitiveNode.isize
            case PrimitiveType.USize:
                return TypePrimitiveNode.usize
            case _:
                assert_never(node.kind)

    # --Declarations--
    def visit_variable(self, node: UnresolvedVariableNode) -> NoReturn:
        assert False, "Tried calling `Type Factory` with a declaration."

    # --Statements--
    def visit_conditional(self, node: UnresolvedConditionalNode) -> NoReturn:
        assert False, "Tried calling `Type Factory` with a statement."

    def visit_expression(self, node: UnresolvedExpressionNode) -> NoReturn:
        assert False, "Tried calling `Type Factory` with a statement."

    # --Expressions--
    def visit_group(self, node: UnresolvedGroupNode) -> TypeNode:
        return node.inner.accept(self)

    def visit_assignment(self, node: UnresolvedAssignNode) -> NoReturn:
        assert False, "Tried calling `Type Factory` with an assignment expression."

    def visit_binary(self, node: UnresolvedBinaryNode) -> NoReturn:
        assert False, "Tried calling `Type Factory` with a binary expression."

    def visit_unary(self, node: UnresolvedUnaryPrefixNode) -> NoReturn:
        assert False, "Tried calling `Type Factory` with a unary expression."

    def visit_identifier(self, node: UnresolvedIdentifierNode) -> NoReturn:
        assert False, "Tried calling `Type Factory` with an identifier."

    # --Extensions--
    def visit_sequence(self, node: UnresolvedSequenceNode) -> NoReturn:
        assert False, "Tried calling `Type Factory` with a sequence."

    def visit_literal(self, node: UnresolvedLiteralNode) -> NoReturn:
        assert False, "Tried calling `Type Factory` with a literal."

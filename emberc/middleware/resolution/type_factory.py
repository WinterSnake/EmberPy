##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolution: Type Factory      ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import TYPE_CHECKING
from ...ast import (
    # -Unresolved
    UnresolvedNodeVisitor, UnresolvedDefaultVisitorMixin,
    UnresolvedTypeNode,
    UnresolvedUnaryPrefixNode, UnresolvedUnaryPostfixNode,
    UnresolvedGroupNode,
    # -Resolved
    NodeType, NodeTypePrimitive,
    NodeTypePointer, NodeTypeSlice,
    NodeTypePendingArray, NodeTypeIdentifier,
)

if TYPE_CHECKING:
    from ..symbol_table import SymbolTable
    from ...ast import UnresolvedUnitNode, UnresolvedIdentifierNode


## Classes
class TypeFactoryVisitor(
    UnresolvedDefaultVisitorMixin[NodeType],
    UnresolvedNodeVisitor[NodeType | None]
):
    """
    Type Factory Resolver

    Walks a type expression and builds a nested resolved or pending
    typed node for a resolved AST tree
    """

    # -Constructor
    def __init__(self, symbol_table: SymbolTable) -> None:
        self._symbol_table = symbol_table

    # -Instance Methods
    def run(self, ast: UnresolvedUnitNode) -> None:
        raise RuntimeError("TypeFactoryVisitor is not meant to run standalone")

    def visit_type(self, node: UnresolvedTypeNode) -> NodeType:
        match node.type:
            case UnresolvedTypeNode.Type.Void:
                return NodeTypePrimitive.void
            case UnresolvedTypeNode.Type.Boolean:
                return NodeTypePrimitive.boolean
            case UnresolvedTypeNode.Type.Int8:
                return NodeTypePrimitive.int8
            case UnresolvedTypeNode.Type.Int16:
                return NodeTypePrimitive.int16
            case UnresolvedTypeNode.Type.Int32:
                return NodeTypePrimitive.int32
            case UnresolvedTypeNode.Type.Int64:
                return NodeTypePrimitive.int64
            case UnresolvedTypeNode.Type.UInt8:
                return NodeTypePrimitive.uint8
            case UnresolvedTypeNode.Type.UInt16:
                return NodeTypePrimitive.uint16
            case UnresolvedTypeNode.Type.UInt32:
                return NodeTypePrimitive.uint32
            case UnresolvedTypeNode.Type.UInt64:
                return NodeTypePrimitive.uint64

    def visit_unary_prefix(self, node: UnresolvedUnaryPrefixNode) -> NodeType:
        target = self.visit(node.operand)
        assert isinstance(target, NodeType), "TODO: Error handling"
        match node.operator:
            case UnresolvedUnaryPrefixNode.Operator.Ptr:
                return NodeTypePointer(target)
            case UnresolvedUnaryPrefixNode.Operator.Slice:
                return NodeTypeSlice(False, target)
            case UnresolvedUnaryPrefixNode.Operator.SlicePtr:
                return NodeTypeSlice(True, target)
            case _:
                assert False, "TODO: Error handling"

    def visit_unary_postfix(self, node: UnresolvedUnaryPostfixNode) -> NodeType:
        if node.kind != UnresolvedUnaryPostfixNode.Kind.Subscript:
            assert False, "TODO: Error handling"
        head = self.visit(node.head)
        assert head is not None, "TODO: Error handling"
        return NodeTypePendingArray(head, node.arguments)

    def visit_group(self, node: UnresolvedGroupNode) -> NodeType:
        assert not node.has_target, "TODO: Error handling"
        inner = self.visit(node.inner)
        assert inner is not None
        return inner

    def visit_identifier(self, node: UnresolvedIdentifierNode) -> NodeType:
        _id = self._symbol_table.find(node.name)
        assert _id is not None, "TODO: Error handling"
        return NodeTypeIdentifier.from_id(_id)

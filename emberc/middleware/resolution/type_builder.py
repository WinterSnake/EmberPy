##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolution: Type Factory      ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING
from ...ast import (
    # -Unresolved
    UnresolvedNodeVisitor,
    UnresolvedNullVisitorMixin,
    UnresolvedTypeNode,
    UnresolvedUnaryPrefixNode,
    # -Resolved
    TypeNode,
    PrimitiveTypeNode,
)

if TYPE_CHECKING:
    from ..symbol_table import SymbolTable
    from ...ast import UnresolvedNode


## Classes
class TypeBuilderFactory(
    UnresolvedNullVisitorMixin[TypeNode],
    UnresolvedNodeVisitor[TypeNode | None]
):
    """
    Type Builder 

    A specialized visitor that transforms an UnresolvedNode into
    a resolved (but possibly pending) TypeNode.
    """

    # -Constructor
    def __init__(self, symbol_table: SymbolTable) -> None:
        self._symbol_table: SymbolTable = symbol_table

    # -Instance Methods
    def run(self, node: UnresolvedNode) -> TypeNode:
        _type = self.visit(node)
        assert _type is not None, "TODO: Error handling"
        return _type
    
    # -Instance Methods: Visitor
    def visit_type(self, node: UnresolvedTypeNode) -> TypeNode:
        match node.kind:
            case UnresolvedTypeNode.Kind.Void:
                return PrimitiveTypeNode.void
            case UnresolvedTypeNode.Kind.Boolean:
                return PrimitiveTypeNode.boolean
            case UnresolvedTypeNode.Kind.Int8:
                return PrimitiveTypeNode.int8
            case UnresolvedTypeNode.Kind.Int16:
                return PrimitiveTypeNode.int16
            case UnresolvedTypeNode.Kind.Int32:
                return PrimitiveTypeNode.int32
            case UnresolvedTypeNode.Kind.Int64:
                return PrimitiveTypeNode.int64
            case UnresolvedTypeNode.Kind.UInt8:
                return PrimitiveTypeNode.uint8
            case UnresolvedTypeNode.Kind.UInt16:
                return PrimitiveTypeNode.uint16
            case UnresolvedTypeNode.Kind.UInt32:
                return PrimitiveTypeNode.uint32
            case UnresolvedTypeNode.Kind.UInt64:
                return PrimitiveTypeNode.uint64
            case UnresolvedTypeNode.Kind.SSize:
                return PrimitiveTypeNode.ssize
            case UnresolvedTypeNode.Kind.USize:
                return PrimitiveTypeNode.usize
            case UnresolvedTypeNode.Kind.Function:
                return PrimitiveTypeNode.function

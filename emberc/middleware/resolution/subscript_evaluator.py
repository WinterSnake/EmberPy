##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolution: Array Eval        ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import TYPE_CHECKING
from .constant_evaluator import ConstantEvaluatorVisitor
from .type_factory import TypeFactoryVisitor
from ...ast import (
    # -Unresolved
    UnresolvedNode,
    UnresolvedNodeVisitor, UnresolvedDefaultVisitorMixin,
    # -Resolved
    NodeTypeArray, NodeTypePendingArray
)

if TYPE_CHECKING:
    from ..symbol_table import SymbolTable
    from ...ast import (
        # -Unresolved
        UnresolvedUnitNode,
        UnresolvedGroupNode, UnresolvedExprEmptyNode,
        UnresolvedBinaryNode,
        UnresolvedUnaryPrefixNode, UnresolvedUnaryPostfixNode,
        UnresolvedIdentifierNode, UnresolvedLiteralNode, UnresolvedArrayNode,
        # -Resolved
        NodeType,
        NodeTypePrimitive, NodeTypeIdentifier,
        NodeTypePointer, NodeTypeSlice, NodeTypeFunction
    )


## Classes
class SubscriptFinalizerVisitor(
    UnresolvedDefaultVisitorMixin[bool],
    UnresolvedNodeVisitor[bool | None]
):
    """
    Array Type Resolver

    Walks a pending array type and builds a finalized array typed node
    """

    # -Constructor
    def __init__(
        self, symbol_table: SymbolTable,
        initializers: dict[int, UnresolvedNode]
    ) -> None:
        self._current_initializer: UnresolvedNode | None = None
        self._symbol_table = symbol_table
        self._constant_eval = ConstantEvaluatorVisitor(symbol_table, initializers)
        self._shape_eval = ShapeEvaluatorVisitor()

    # -Instance Methods: Initializer
    def reset_initializer(self) -> None:
        self._current_initializer = None

    # -Instance Methods: UnresolvedNode Visitor
    def run(self, ast: UnresolvedUnitNode) -> None:
        raise RuntimeError("SubscriptFinalizerVisitor is not meant to run standalone")

    def visit_expr_empty(self, node: UnresolvedExprEmptyNode) -> bool:
        return False

    def visit_binary(self, node: UnresolvedBinaryNode) -> bool:
        return True

    def visit_unary_prefix(self, node: UnresolvedUnaryPrefixNode) -> bool:
        return True

    def visit_unary_postfix(self, node: UnresolvedUnaryPostfixNode) -> bool:
        return True

    def visit_group(self, node: UnresolvedGroupNode) -> bool:
        return True

    def visit_literal(self, node: UnresolvedLiteralNode) -> bool:
        return True

    def visit_identifier(self, node: UnresolvedIdentifierNode) -> bool:
        return True

    # -Instance Methods: TypeNode Visitor
    def visit_type_primitive(self, node: NodeTypePrimitive) -> NodeType:
        return node

    def visit_type_array(self, node: NodeTypeArray) -> NodeType:
        node.target = node.target.accept(self)
        return node

    def visit_type_identifier(self, node: NodeTypeIdentifier) -> NodeType:
        return node

    def visit_type_function(self, node: NodeTypeFunction) -> NodeType:
        node.return_type = node.return_type.accept(self)
        for i, parameter_type in enumerate(node.parameter_types):
            node.parameter_types[i] = parameter_type.accept(self)
        return node

    def visit_type_pointer(self, node: NodeTypePointer) -> NodeType:
        node.target = node.target.accept(self)
        return node

    def visit_type_slice(self, node: NodeTypeSlice) -> NodeType:
        node.target = node.target.accept(self)
        return node

    def visit_type_array_pending(self, node: NodeTypePendingArray) -> NodeType:
        # -Jagged array
        if isinstance(node.target, NodeTypePendingArray):
            assert len(node.dimensions) == 1, "TODO: Error handling"
            assert not self.visit(node.dimensions[0]), "TODO: Error handling"
            return NodeTypeArray(node.target.accept(self), tuple(), True)
        # -Flat or Ranked array
        final_dimensions: list[int] = []
        # -Static size
        static_dimensions: list[int | None] = []
        for dimension in node.dimensions:
            size: int | None
            if self.visit(dimension):
                size = self._constant_eval.get_value(dimension)
            else:
                size = None
            static_dimensions.append(size)
        # -Initializer sizing
        if self.has_initializer:
            inferred_dimensions = self._shape_eval.visit(self.current_initializer)
            assert inferred_dimensions is not None, "TODO: Error handling"
            assert len(inferred_dimensions) == len(static_dimensions), "TODO: Error handling"
            for static, inferred in zip(static_dimensions, inferred_dimensions):
                if static is None:
                    final_dimensions.append(inferred)
                else:
                    assert static == inferred, "TODO: Error handling"
                    final_dimensions.append(static)
        # -Static sizing
        else:
            for static in static_dimensions:
                assert static is not None, "TODO: Error handling"
                final_dimensions.append(static)
        return NodeTypeArray(
            node.target.accept(self), tuple(final_dimensions)
        )

    # -Properties
    @property
    def current_initializer(self) -> UnresolvedNode:
        assert self._current_initializer is not None
        return self._current_initializer

    @current_initializer.setter
    def current_initializer(self, value: UnresolvedNode) -> None:
        self._current_initializer = value

    @property
    def has_initializer(self) -> bool:
        return self._current_initializer is not None


class ShapeEvaluatorVisitor(
    UnresolvedDefaultVisitorMixin[tuple[int, ...]],
    UnresolvedNodeVisitor[tuple[int, ...] | None]
):
    """
    Shape Type Resolver

    Walks a variable initializer (specifically array initializers)
    and produces the rectangular shape to describe the type constraints
    """

    # -Instance Methods
    def run(self, ast: UnresolvedUnitNode) -> None:
        raise RuntimeError("ShapeEvaluatorVisitor is not meant to run standalone")

    def visit_array(self, node: UnresolvedArrayNode) -> tuple[int, ...]:
        outer_dimension = len(node.values)
        assert outer_dimension > 0, "TODO: Error handling"
        inner_dimension = self.visit(node.values[0])
        if inner_dimension is None:
            for i in range(1, outer_dimension):
                assert self.visit(node.values[i]) is None, "TODO: Error handling"
            return (outer_dimension,)
        for i in range(1, outer_dimension):
            assert self.visit(node.values[i]) == inner_dimension, "TODO: Error handling"
        return (outer_dimension, *inner_dimension)

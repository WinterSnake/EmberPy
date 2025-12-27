##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolution: Constant Eval     ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import TYPE_CHECKING
from ...ast import (
    UnresolvedNode,
    UnresolvedBinaryNode,
    UnresolvedUnaryPrefixNode, UnresolvedUnaryPostfixNode,
    UnresolvedNodeVisitor, UnresolvedDefaultVisitorMixin
)

if TYPE_CHECKING:
    from ..symbol_table import SymbolTable
    from ...ast import (
        UnresolvedUnitNode,
        UnresolvedGroupNode, UnresolvedExprEmptyNode,
        UnresolvedIdentifierNode, UnresolvedLiteralNode, UnresolvedArrayNode,
        UnresolvedNodeVisitor, UnresolvedDefaultVisitorMixin
    )


## Classes
class ConstantEvaluatorVisitor(
    UnresolvedDefaultVisitorMixin[int],
    UnresolvedNodeVisitor[int | None]
):
    """
    Constant Fold Evaluator

    Walks a constant expression (including identifier's with initialization)
    and returns the constant int value from the given expression
    """

    # -Constructor
    def __init__(
        self, symbol_table: SymbolTable,
        initializers: dict[int, UnresolvedNode]
    ) -> None:
        self._symbol_table = symbol_table
        self._initializers: dict[int, UnresolvedNode] = initializers

    # -Instance Methods
    def get_value(self, node: UnresolvedNode) -> int:
        value = self.visit(node)
        assert value is not None, "TODO: Error handling"
        return value

    # -Instance Methods: Visitor
    def run(self, ast: UnresolvedUnitNode) -> None:
        raise RuntimeError("ConstantEvaluatorVisitor is not meant to run standalone")

    def visit_binary(self, node: UnresolvedBinaryNode) -> int:
        lhs = self.visit(node.lhs)
        rhs = self.visit(node.rhs)
        assert lhs is not None and rhs is not None
        match node.operator:
            case UnresolvedBinaryNode.Operator.Add:
                return lhs + rhs
            case UnresolvedBinaryNode.Operator.Sub:
                return lhs - rhs
            case UnresolvedBinaryNode.Operator.Mul:
                return lhs * rhs
            case UnresolvedBinaryNode.Operator.Div:
                return lhs // rhs
            case UnresolvedBinaryNode.Operator.Mod:
                return lhs % rhs
            case UnresolvedBinaryNode.Operator.BitXor:
                return lhs ^ rhs
            case UnresolvedBinaryNode.Operator.BitAnd:
                return lhs & rhs
            case UnresolvedBinaryNode.Operator.BitOr:
                return lhs | rhs
            case UnresolvedBinaryNode.Operator.ShiftL:
                return lhs << rhs
            case UnresolvedBinaryNode.Operator.ShiftR:
                return lhs >> rhs
        assert False, "TODO: Error handling"

    def visit_unary_prefix(self, node: UnresolvedUnaryPrefixNode) -> int:
        operand = self.visit(node.operand)
        assert operand is not None
        match node.operator:
            case UnresolvedUnaryPrefixNode.Operator.Negative:
                return -operand
        assert False, "TODO: Error handling"

    def visit_group(self, node: UnresolvedGroupNode) -> int:
        inner = self.visit(node.inner)
        assert inner is not None, "TODO: Error handling"
        if not node.has_target:
            return inner
        assert isinstance(node.target, UnresolvedUnaryPrefixNode), "TODO: Error handling"
        target = self.visit(node.target.operand)
        assert target is not None, "TODO: Error handling"
        match node.target.operator:
            case UnresolvedUnaryPrefixNode.Operator.Negative:
                return inner - target
            case UnresolvedUnaryPrefixNode.Operator.Ptr:
                return inner * target
            case UnresolvedUnaryPrefixNode.Operator.Deref:
                return inner ^ target
        assert False, "TODO: Error handling"

    def visit_unary_postfix(self, node: UnresolvedUnaryPostfixNode) -> int:
        assert False, "TODO"

    def visit_literal(self, node: UnresolvedLiteralNode) -> int:
        assert isinstance(node.value, int), "TODO: Error handling"
        return node.value

    def visit_array(self, node: UnresolvedArrayNode) -> int:
        assert False, "TODO"

    def visit_identifier(self, node: UnresolvedIdentifierNode) -> int:
        symbol = self._symbol_table.get(node.id)
        if symbol.has_value:
            assert isinstance(symbol.value, int), "TODO: Error handling"
            return symbol.value
        elif node.id in self._initializers:
            symbol._value = self.visit(self._initializers[node.id])
            assert isinstance(symbol.value, int), "TODO: Error handling"
            return symbol.value
        assert False, "TODO: Error handling"

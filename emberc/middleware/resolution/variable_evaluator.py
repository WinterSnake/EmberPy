##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolution: Variable Eval     ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Iterator
from typing import TYPE_CHECKING
from ...ast import UnresolvedNodeVisitor, UnresolvedDefaultVisitorMixin

if TYPE_CHECKING:
    from ..symbol_table import SymbolTable
    from ...ast import (
        UnresolvedDeclVariableNode,
        UnresolvedNode, UnresolvedUnitNode, UnresolvedTypeNode,
        UnresolvedGroupNode, UnresolvedExprEmptyNode,
        UnresolvedAssignNode, UnresolvedBinaryNode,
        UnresolvedUnaryPrefixNode, UnresolvedUnaryPostfixNode,
        UnresolvedIdentifierNode, UnresolvedLiteralNode, UnresolvedArrayNode,
    )


## Classes
class VariableEvaluatorVisitor(
    UnresolvedDefaultVisitorMixin[Iterator[int]],
    UnresolvedNodeVisitor[Iterator[int] | None]
):
    """
    Variable Validation Evaluator
    
    Walks a variable declaration left to right to check
    if initializer dependencies are logically scoped in addition to
    checking if the node's type has a cyclical dependency of it's own entries
    """

    # -Instance Methods
    def run(self, ast: UnresolvedUnitNode) -> None:
        raise RuntimeError("VariableEvaluatorVisitor is not meant to run standalone")

    def validate(self, variable: UnresolvedDeclVariableNode) -> bool:
        known = set(entry.id for entry in variable.entries)
        current = []
        for _id in self._visit_iterator(variable.type):
            if _id in known:
                return False
        for entry in variable.entries:
            if entry.has_initializer:
                for _id in self._visit_iterator(entry.initializer):
                    if _id not in known:
                        continue
                    if _id not in current:
                        return False
            current.append(entry.id)
        return True

    def _visit_iterator(self, node: UnresolvedNode) -> Iterator[int]:
        iterator = self.visit(node)
        assert iterator is not None, "TODO: Error handling"
        yield from iterator

    def visit_type(self, node: UnresolvedTypeNode) -> Iterator[int]:
        return
        yield

    def visit_expr_empty(self, node: UnresolvedExprEmptyNode) -> Iterator[int]:
        return
        yield

    def visit_assignment(self, node: UnresolvedAssignNode) -> Iterator[int]:
        yield from self._visit_iterator(node.l_value)
        yield from self._visit_iterator(node.r_value)

    def visit_binary(self, node: UnresolvedBinaryNode) -> Iterator[int]:
        yield from self._visit_iterator(node.lhs)
        yield from self._visit_iterator(node.rhs)

    def visit_unary_prefix(self, node: UnresolvedUnaryPrefixNode) -> Iterator[int]:
        yield from self._visit_iterator(node.operand)

    def visit_unary_postfix(self, node: UnresolvedUnaryPostfixNode) -> Iterator[int]:
        yield from self._visit_iterator(node.head)
        for argument in node.arguments:
            yield from self._visit_iterator(argument)

    def visit_group(self, node: UnresolvedGroupNode) -> Iterator[int]:
        yield from self._visit_iterator(node.inner)
        if node.has_target:
            yield from self._visit_iterator(node.target)

    def visit_array(self, node: UnresolvedArrayNode) -> Iterator[int]:
        for value in node.values:
            yield from self._visit_iterator(value)

    def visit_literal(self, node: UnresolvedLiteralNode) -> Iterator[int]:
        return
        yield

    def visit_identifier(self, node: UnresolvedIdentifierNode) -> Iterator[int]:
        yield node.id

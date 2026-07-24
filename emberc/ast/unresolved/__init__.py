##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## AST: Unresolved               ##
##-------------------------------##

## Imports
from abc import ABC, abstractmethod
from typing import Protocol
from .binary import (
    UnresolvedAssignNode,
    UnresolvedBinaryNode,
)
from .conditional import UnresolvedConditionalNode
from .expression import (
    UnresolvedExpressionNode,
    UnresolvedGroupNode,
)
from .literal import (
    UnresolvedLiteralNode,
    UnresolvedBooleanNode,
    UnresolvedIntegerNode,
)
from .node import UnresolvedNode
from .sequence import (
    UnresolvedSequenceNode,
    UnresolvedUnitNode,
    UnresolvedBlockNode,
)
from .type import UnresolvedTypeNode
from .unary import UnresolvedUnaryPrefixNode
from .variable import (
    UnresolvedIdentifierNode,
    UnresolvedVariableNode,
)

## Constants
__all__ = (
    "UnresolvedNode",
    "UnresolvedSequenceNode",
    "UnresolvedLiteralNode",
    # -Types
    "UnresolvedTypeNode",
    # -Declarations
    "UnresolvedUnitNode",
    "UnresolvedVariableNode",
    # -Statements
    "UnresolvedBlockNode",
    "UnresolvedConditionalNode",
    "UnresolvedExpressionNode",
    # -Expressions
    "UnresolvedGroupNode",
    "UnresolvedAssignNode",
    "UnresolvedBinaryNode",
    "UnresolvedUnaryPrefixNode",
    "UnresolvedBooleanNode",
    "UnresolvedIntegerNode",
    "UnresolvedIdentifierNode",
    # -Visitor
    "UnresolvedNodeVisitor",
    "UnresolvedSequenceRouterMixin",
    "UnresolvedLiteralRouterMixin",
)


## Classes
class UnresolvedNodeVisitor[R](Protocol):
    """Unresolved AST node visitor interface."""
    # -Instance Methods
    # --Types--
    def visit_type(self, node: UnresolvedTypeNode) -> R: ...
    # --Declarations--
    def visit_unit(self, node: UnresolvedUnitNode) -> R: ...
    def visit_variable(self, node: UnresolvedVariableNode) -> R: ...
    # --Statements--
    def visit_block(self, node: UnresolvedBlockNode) -> R: ...
    def visit_conditional(self, node: UnresolvedConditionalNode) -> R: ...
    def visit_expression(self, node: UnresolvedExpressionNode) -> R: ...
    # --Expressions--
    def visit_group(self, node: UnresolvedGroupNode) -> R: ...
    def visit_assignment(self, node: UnresolvedAssignNode) -> R: ...
    def visit_binary(self, node: UnresolvedBinaryNode) -> R: ...
    def visit_unary(self, node: UnresolvedUnaryPrefixNode) -> R: ...
    def visit_boolean(self, node: UnresolvedBooleanNode) -> R: ...
    def visit_integer(self, node: UnresolvedIntegerNode) -> R: ...
    def visit_identifier(self, node: UnresolvedIdentifierNode) -> R: ...


class UnresolvedLiteralRouterMixin[R](UnresolvedNodeVisitor[R], ABC):
    """Unresolved visitor mixin for delegating all literal node calls to a single entry."""
    # -Instance Methods
    @abstractmethod
    def visit_literal(self, node: UnresolvedLiteralNode) -> R: ...

    def visit_boolean(self, node: UnresolvedBooleanNode) -> R:
        return self.visit_literal(node)

    def visit_integer(self, node: UnresolvedIntegerNode) -> R:
        return self.visit_literal(node)


class UnresolvedSequenceRouterMixin[R](UnresolvedNodeVisitor[R], ABC):
    """Unresolved visitor mixin for delegating all sequence node calls to a single entry."""
    # -Instance Methods
    @abstractmethod
    def visit_sequence(self, node: UnresolvedSequenceNode) -> R: ...

    def visit_unit(self, node: UnresolvedUnitNode) -> R:
        return self.visit_sequence(node)

    def visit_block(self, node: UnresolvedBlockNode) -> R:
        return self.visit_sequence(node)

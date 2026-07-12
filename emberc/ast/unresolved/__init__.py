##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## AST: Unresolved               ##
##-------------------------------##

## Imports
from typing import Protocol
from .binary import (
    UnresolvedAssignNode,
    UnresolvedBinaryNode,
)
from .literal import (
    UnresolvedLiteralNode,
)
from .expression import (
    UnresolvedExprNode,
    UnresolvedGroupNode,
)
from .node import (
    UnresolvedNode,
    UnresolvedUnitNode,
)
from .types import (
    UnresolvedTypeNode,
)
from .variable import (
    UnresolvedIdentifierNode,
    UnresolvedVariableNode,
)

## Constants
__all__ = (
    "UnresolvedNode",
    "UnresolvedNodeVisitor",
    # -Types
    "UnresolvedTypeNode",
    # -Declarations
    "UnresolvedUnitNode",
    "UnresolvedVariableNode",
    # -Statements
    "UnresolvedExprNode",
    # -Expressions
    "UnresolvedGroupNode",
    "UnresolvedAssignNode",
    "UnresolvedBinaryNode",
    "UnresolvedLiteralNode",
    "UnresolvedIdentifierNode",
)


## Classes
class UnresolvedNodeVisitor[TReturn](Protocol):
    """
    A structural protocol implementing the visitor pattern for unresolved AST nodes.
    """
    # -Instance Methods
    # --Types--
    def visit_type(self, node: UnresolvedTypeNode) -> TReturn: ...
    # --Declarations--
    def visit_unit(self, node: UnresolvedUnitNode) -> TReturn: ...
    def visit_variable(self, node: UnresolvedVariableNode) -> TReturn: ...
    # --Statements--
    def visit_expression(self, node: UnresolvedExprNode) -> TReturn: ...
    # --Expressions--
    def visit_group(self, node: UnresolvedGroupNode) -> TReturn: ...
    def visit_assignment(self, node: UnresolvedAssignNode) -> TReturn: ...
    def visit_binary(self, node: UnresolvedBinaryNode) -> TReturn: ...
    def visit_literal(self, node: UnresolvedLiteralNode) -> TReturn: ...
    def visit_identifier(self, node: UnresolvedIdentifierNode) -> TReturn: ...

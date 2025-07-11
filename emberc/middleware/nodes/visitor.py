##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node Visitor                  ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from .statement_unit import NodeStatementUnit
    from .expression_binary import NodeExprBinary
    from .expression_unary import NodeExprUnary
    from .expression_literal import NodeExprLiteral


## Classes
class NodeVisitor(Protocol):
    """
    Ember Node Visitor
    Visitor pattern protocol for handling and evaluating nodes
    """

    # -Instance Methods
    def visit_statement_unit(self, node: NodeStatementUnit) -> Any: ...
    def visit_expression_binary(self, node: NodeExprBinary) -> Any: ...
    def visit_expression_unary(self, node: NodeExprUnary) -> Any: ...
    def visit_expression_literal(self, node: NodeExprLiteral) -> Any: ...

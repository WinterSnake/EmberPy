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
    from .expr_binary import NodeExprBinary
    from .expr_literal import NodeExprLiteral


## Classes
class NodeVisitor(Protocol):
    """
    Ember Node Visitor
    Protocol interface for walking through an AST tree
    """
    
    # -Instance Methods
    def visit_expression_binary(self, node: NodeExprBinary) -> Any: ...
    def visit_expression_literal(self, node: NodeExprLiteral) -> Any: ...

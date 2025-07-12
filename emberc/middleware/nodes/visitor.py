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
    from .core import NodeModule
    from .statement_control import (
        NodeStmtBlock, NodeStmtConditional, NodeStmtLoop
    )
    from .statement_declaration import (
        NodeDeclFunction, NodeDeclVariable, NodeStmtExpression
    )
    from .expression_logic import NodeExprAssignment, NodeExprCall
    from .expression_binary import NodeExprBinary
    from .expression_unary import NodeExprUnary
    from .expression_primary import (
        NodeExprGroup, NodeExprVariable, NodeExprLiteral
    )


## Classes
class NodeVisitor(Protocol):
    """
    Ember Node Visitor
    Protocol for an AST traversal class
    """

    # -Instance Methods
    def visit_module(self, node: NodeModule) -> Any: ...
    def visit_declaration_function(self, node: NodeDeclFunction) -> Any: ...
    def visit_declaration_variable(self, node: NodeDeclVariable) -> Any: ...
    def visit_statement_block(self, node: NodeStmtBlock) -> Any: ...
    def visit_statement_conditional(self, node: NodeStmtConditional) -> Any: ...
    def visit_statement_loop(self, node: NodeStmtLoop) -> Any: ...
    def visit_statement_expression(self, node: NodeStmtExpression) -> Any: ...
    def visit_expression_assignment(self, node: NodeExprAssignment) -> Any: ...
    def visit_expression_binary(self, node: NodeExprBinary) -> Any: ...
    def visit_expression_unary(self, node: NodeExprUnary) -> Any: ...
    def visit_expression_call(self, node: NodeExprCall) -> Any: ...
    def visit_expression_group(self, node: NodeExprGroup) -> Any: ...
    def visit_expression_variable(self, node: NodeExprVariable) -> Any: ...
    def visit_expression_literal(self, node: NodeExprLiteral) -> Any: ...

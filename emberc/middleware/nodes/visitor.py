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
    from .decl_module import NodeDeclModule
    from .decl_variable import NodeDeclVariable
    from .stmt_assignment import NodeStmtAssignment
    from .stmt_expression import NodeStmtExpression
    from .expr_binary import NodeExprBinary
    from .expr_literal import NodeExprLiteral


## Classes
class NodeVisitor(Protocol):
    """
    Ember Node Visitor
    Protocol interface for walking through an AST tree
    """
    
    # -Instance Methods
    def visit_declaration_module(self, node: NodeDeclModule) -> Any: ...
    def visit_declaration_variable(self, node: NodeDeclVariable) -> Any: ...
    def visit_statement_assignment(self, node: NodeStmtAssignment) -> Any: ...
    def visit_statement_expression(self, node: NodeStmtExpression) -> Any: ...
    def visit_expression_binary(self, node: NodeExprBinary) -> Any: ...
    def visit_expression_literal(self, node: NodeExprLiteral) -> Any: ...

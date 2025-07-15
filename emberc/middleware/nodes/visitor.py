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
    from .decl_function import NodeDeclFunction
    from .decl_variable import NodeDeclVariable
    from .stmt_block import NodeStmtBlock
    from .stmt_condition import NodeStmtCondition
    from .stmt_loop import NodeStmtLoop
    from .stmt_expression import NodeStmtExpression
    from .expr_assignment import NodeExprAssignment
    from .expr_binary import NodeExprBinary
    from .expr_unary import NodeExprUnary
    from .expr_group import NodeExprGroup
    from .expr_variable import NodeExprVariable
    from .expr_literal import NodeExprLiteral


## Classes
class NodeVisitor(Protocol):
    """
    Ember Node Visitor
    Protocol interface for walking through an AST tree
    """
    
    # -Instance Methods
    def visit_declaration_module(self, node: NodeDeclModule) -> Any: ...
    def visit_declaration_function(self, node: NodeDeclFunction) -> Any: ...
    def visit_declaration_variable(self, node: NodeDeclVariable) -> Any: ...
    def visit_statement_block(self, node: NodeStmtBlock) -> Any: ...
    def visit_statement_condition(self, node: NodeStmtCondition) -> Any: ...
    def visit_statement_loop(self, node: NodeStmtLoop) -> Any: ...
    def visit_statement_expression(self, node: NodeStmtExpression) -> Any: ...
    def visit_expression_assignment(self, node: NodeExprAssignment) -> Any: ...
    def visit_expression_binary(self, node: NodeExprBinary) -> Any: ...
    def visit_expression_unary(self, node: NodeExprUnary) -> Any: ...
    def visit_expression_group(self, node: NodeExprGroup) -> Any: ...
    def visit_expression_variable(self, node: NodeExprVariable) -> Any: ...
    def visit_expression_literal(self, node: NodeExprLiteral) -> Any: ...

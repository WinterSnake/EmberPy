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
    from .statement_declaration import NodeStmtDeclVar
    from .statement_expression import NodeStmtExpr
    from .expression_assignment import NodeExprAssign
    from .expression_binary import NodeExprBinary
    from .expression_unary import NodeExprUnary
    from .expression_group import NodeExprGroup
    from .expression_literal import NodeExprId, NodeExprLiteral


## Classes
class NodeVisitor(Protocol):
    """
    Ember Node Visitor
    Visitor pattern protocol for handling and evaluating nodes
    """

    # -Instance Methods
    def visit_module(self, node: NodeModule) -> Any: ...
    def visit_statement_declaration_variable(self, node: NodeStmtDeclVar) -> Any: ...
    def visit_statement_expression(self, node: NodeStmtExpr) -> Any: ...
    def visit_expression_assign(self, node: NodeExprAssign) -> Any: ...
    def visit_expression_binary(self, node: NodeExprBinary) -> Any: ...
    def visit_expression_unary(self, node: NodeExprUnary) -> Any: ...
    def visit_expression_group(self, node: NodeExprGroup) -> Any: ...
    def visit_expression_id(self, node: NodeExprId) -> Any: ...
    def visit_expression_literal(self, node: NodeExprLiteral) -> Any: ...

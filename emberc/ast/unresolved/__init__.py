##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## AST: Unresolved               ##
##-------------------------------##

## Imports
from .assign import UnresolvedAssignNode
from .binary import UnresolvedBinaryNode
from .declaration import (
    UnresolvedDeclNode,
    UnresolvedDeclFunctionNode,
    UnresolvedDeclVariableNode,
)
from .group import UnresolvedGroupNode
from .identifier import UnresolvedIdentifierNode
from .literal import (
    LITERAL_VALUE,
    UnresolvedLiteralNode,
    UnresolvedArrayNode,
    UnresolvedExprEmptyNode
)
from .node import (
    UnresolvedNode,
    UnresolvedTypeNode,
    UnresolvedUnitNode
)
from .statement import (
    BLOCK_TYPES,
    UnresolvedStmtNode,
    UnresolvedStmtBlockNode,
    UnresolvedStmtExpressionNode,
    UnresolvedStmtConditionalNode,
    UnresolvedStmtLoopWhileNode,
    UnresolvedStmtLoopDoNode,
    UnresolvedStmtLoopForNode,
    UnresolvedStmtReturnNode,
    UnresolvedStmtEmptyNode,
)
from .unary import (
    UnresolvedUnaryPrefixNode,
    UnresolvedUnaryModifierNode,
    UnresolvedUnaryPostfixNode
)
from .visitor import UnresolvedNodeVisitor

## Constants
__all__ = (
    "BLOCK_TYPES",
    "LITERAL_VALUE",
    "UnresolvedNode",
    "UnresolvedUnitNode",
    "UnresolvedTypeNode",
    "UnresolvedDeclNode",
    "UnresolvedStmtNode",
    "UnresolvedDeclFunctionNode",
    "UnresolvedDeclVariableNode",
    "UnresolvedStmtBlockNode",
    "UnresolvedStmtExpressionNode",
    "UnresolvedStmtConditionalNode",
    "UnresolvedStmtLoopWhileNode",
    "UnresolvedStmtLoopDoNode",
    "UnresolvedStmtLoopForNode",
    "UnresolvedStmtReturnNode",
    "UnresolvedStmtEmptyNode",
    "UnresolvedGroupNode",
    "UnresolvedExprEmptyNode",
    "UnresolvedAssignNode",
    "UnresolvedBinaryNode",
    "UnresolvedUnaryModifierNode",
    "UnresolvedUnaryPrefixNode",
    "UnresolvedUnaryPostfixNode",
    "UnresolvedIdentifierNode",
    "UnresolvedLiteralNode",
    "UnresolvedArrayNode",
    "UnresolvedNodeVisitor",
    "UnresolvedDefaultVisitorMixin",
)


## Classes
class UnresolvedDefaultVisitorMixin[TReturn]:
    """
    Ember Unresolved Visitor: Default Mixin

    Handles default implementation for all visit methods
    as optional TReturn by returning None
    """
    # -Instance Methods
    def visit_type(self, node: UnresolvedTypeNode) -> TReturn | None:
        return None
    def visit_decl_function(self, node: UnresolvedDeclFunctionNode) -> TReturn | None:
        return None
    def visit_decl_variable(self, node: UnresolvedDeclVariableNode) -> TReturn | None:
        return None
    def visit_stmt_empty(self, node: UnresolvedStmtEmptyNode) -> TReturn | None:
        return None
    def visit_stmt_block(self, node: UnresolvedStmtBlockNode) -> TReturn | None:
        return None
    def visit_stmt_condition(self, node: UnresolvedStmtConditionalNode) -> TReturn | None:
        return None
    def visit_stmt_loop_while(self, node: UnresolvedStmtLoopWhileNode) -> TReturn | None:
        return None
    def visit_stmt_loop_do(self, node: UnresolvedStmtLoopDoNode) -> TReturn | None:
        return None
    def visit_stmt_loop_for(self, node: UnresolvedStmtLoopForNode) -> TReturn | None:
        return None
    def visit_stmt_return(self, node: UnresolvedStmtReturnNode) -> TReturn | None:
        return None
    def visit_stmt_expression(self, node: UnresolvedStmtExpressionNode) -> TReturn | None:
        return None
    def visit_expr_empty(self, node: UnresolvedExprEmptyNode) -> TReturn | None:
        return None
    def visit_assignment(self, node: UnresolvedAssignNode) -> TReturn | None:
        return None
    def visit_binary(self, node: UnresolvedBinaryNode) -> TReturn | None:
        return None
    def visit_unary_modifier(self, node: UnresolvedUnaryModifierNode) -> TReturn | None:
        return None
    def visit_unary_prefix(self, node: UnresolvedUnaryPrefixNode) -> TReturn | None:
        return None
    def visit_unary_postfix(self, node: UnresolvedUnaryPostfixNode) -> TReturn | None:
        return None
    def visit_group(self, node: UnresolvedGroupNode) -> TReturn | None:
        return None
    def visit_array(self, node: UnresolvedArrayNode) -> TReturn | None:
        return None
    def visit_literal(self, node: UnresolvedLiteralNode) -> TReturn | None:
        return None
    def visit_identifier(self, node: UnresolvedIdentifierNode) -> TReturn | None:
        return None

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Middleware: Visitor           ##
##-------------------------------##

## Imports
from .decl import NodeDeclVisitor
from .expr import NodeExprVisitor
from .stmt import NodeStmtVisitor
from .typed import NodeTypeVisitor
from .visitor import NodeVisitor

## Constants
__all__ = (
    "NodeVisitor",
    "NodeTypeVisitor", "NodeDeclVisitor",
    "NodeStmtVisitor", "NodeExprVisitor",
    "null_type_visitor", "null_decl_visitor",
    "null_stmt_visitor", "null_expr_visitor",
)


## Classes
class NullTypeVisitor:
    """Type Visitor: No-op"""
    # -Instance Methods
    def visit_type_builtin(self, node, manager) -> None:
        return None
    def visit_type_custom(self, node, manager) -> None:
        return None


class NullDeclVisitor:
    """Decl Visitor: No-op"""
    # -Instance Methods
    def visit_decl_unit(self, node, manager) -> None:
        return None
    def visit_decl_function(self, node, manager) -> None:
        return None
    def visit_decl_variable(self, node, manager) -> None:
        return None


class NullStmtVisitor:
    """Stmt Visitor: No-op"""
    # -Instance Methods
    def visit_stmt_block(self, node, manager) -> None:
        return None
    def visit_stmt_conditional(self, node, manager) -> None:
        return None
    def visit_stmt_loop(self, node, manager) -> None:
        return None
    def visit_stmt_return(self, node, manager) -> None:
        return None
    def visit_stmt_expression(self, node, manager) -> None:
        return None


class NullExprVisitor:
    """Expr Visitor: No-op"""
    # -Instance Methods
    def visit_expr_assignment(self, node, manager) -> None:
        return None
    def visit_expr_group(self, node, manager) -> None:
        return None
    def visit_expr_binary(self, node, manager) -> None:
        return None
    def visit_expr_unary(self, node, manager) -> None:
        return None
    def visit_expr_call(self, node, manager) -> None:
        return None
    def visit_expr_literal(self, node, manager) -> None:
        return None
    def visit_expr_variable(self, node, manager) -> None:
        return None


## Body
null_type_visitor = NullTypeVisitor()
null_decl_visitor = NullDeclVisitor()
null_stmt_visitor = NullStmtVisitor()
null_expr_visitor = NullExprVisitor()

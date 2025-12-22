##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Visitor                       ##
##-------------------------------##

## Imports
from ..nodes import NodeDecl, NodeStmt, NodeExpr
from .decl import NodeDeclVisitor
from .expr import NodeExprVisitor
from .stmt import NodeStmtVisitor

## Classes
class NodeVisitor[TDecl, TStmt, TExpr]:
    """
    Node Visitor

    The master node visitor and manager for handling sub-typed specific node visitors
    """

    # -Constructor
    def __init__(
        self, decl_v: NodeDeclVisitor[TDecl], stmt_v: NodeStmtVisitor[TStmt],
        expr_v: NodeExprVisitor[TExpr]
    ) -> None:
        self._decl_v: NodeDeclVisitor[TDecl] = decl_v
        self._stmt_v: NodeStmtVisitor[TStmt] = stmt_v
        self._expr_v: NodeExprVisitor[TExpr] = expr_v

    # -Instance Methods
    def visit_declaration(self, node: NodeDecl) -> TDecl:
        return node.accept(self._decl_v, self)

    def visit_statement(self, node: NodeStmt) -> TStmt:
        return node.accept(self._stmt_v, self)

    def visit_expression(self, node: NodeExpr) -> TExpr:
        return node.accept(self._expr_v, self)

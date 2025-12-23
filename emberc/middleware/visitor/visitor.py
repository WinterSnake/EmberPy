##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Visitor                       ##
##-------------------------------##

## Imports
from ..nodes import (
    NodeBase, NodeType, NodeDecl, NodeStmt, NodeExpr,
    NodeDeclUnit, 
)
from .decl import NodeDeclVisitor
from .expr import NodeExprVisitor
from .stmt import NodeStmtVisitor
from .typed import NodeTypeVisitor

## Classes
class NodeVisitor[TType, TDecl, TStmt, TExpr]:
    """
    Node Visitor

    The master node visitor and manager for handling sub-typed specific node visitors
    """

    # -Constructor
    def __init__(
        self, type_v: NodeTypeVisitor[TType], decl_v: NodeDeclVisitor[TDecl],
        stmt_v: NodeStmtVisitor[TStmt], expr_v: NodeExprVisitor[TExpr]
    ) -> None:
        self._type_v: NodeTypeVisitor[TType] = type_v
        self._decl_v: NodeDeclVisitor[TDecl] = decl_v
        self._stmt_v: NodeStmtVisitor[TStmt] = stmt_v
        self._expr_v: NodeExprVisitor[TExpr] = expr_v

    # -Instance Methods
    def run(self, ast: NodeDeclUnit) -> TDecl:
        return self.visit_declaration(ast)

    def visit(self, node: NodeBase) -> TType | TDecl | TStmt | TExpr:
        match node:
            case NodeType():
                return self.visit_type(node)
            case NodeDecl():
                return self.visit_declaration(node)
            case NodeStmt():
                return self.visit_statement(node)
            case NodeExpr():
                return self.visit_expression(node)
            case _:
                raise RuntimeError(f"Unhandled node type: {node} in visitor")

    def visit_type(self, node: NodeType) -> TType:
        return node.accept(self._type_v, self)

    def visit_declaration(self, node: NodeDecl) -> TDecl:
        return node.accept(self._decl_v, self)

    def visit_statement(self, node: NodeStmt) -> TStmt:
        return node.accept(self._stmt_v, self)

    def visit_expression(self, node: NodeExpr) -> TExpr:
        return node.accept(self._expr_v, self)

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## AST: Resolved                 ##
##-------------------------------##

## Imports
from typing import Protocol
from .declarations import (
    DeclNode,
    DeclUnitNode,
    DeclSequenceNode,
    DeclVariableNode,
    DeclNodeVisitor,
)
from .expressions import (
    ExprNode,
    ExprAssignNode,
    ExprBinaryNode,
    ExprIntegerNode,
    ExprVariableNode,
    ExprNodeVisitor,
)
from .statements import (
    StmtNode,
    StmtEmptyNode,
    StmtExpressionNode,
    StmtNodeVisitor,
)
from .types import (
    TypeNode,
    TypePending,
    TypePrimitive,
    TypeNodeVisitor,
)

## Constants
__all__ = (
    "ResolvedNode",
    "ResolvedNodeVisitor",
    # -Types
    "TypeNode",
    "TypePending",
    "TypePrimitive",
    "TypeNodeVisitor",
    # -Declarations
    "DeclNode",
    "DeclUnitNode",
    "DeclSequenceNode",
    "DeclVariableNode",
    "DeclNodeVisitor",
    # -Statements
    "StmtNode",
    "StmtEmptyNode",
    "StmtExpressionNode",
    "StmtNodeVisitor",
    # -Expressions
    "ExprNode",
    "ExprAssignNode",
    "ExprBinaryNode",
    "ExprIntegerNode",
    "ExprVariableNode",
    "ExprNodeVisitor",
)
type ResolvedNode = TypeNode | DeclNode | StmtNode | ExprNode


## Classes
class ResolvedNodeVisitor[TType, TDecl, TStmt, TExpr](
    TypeNodeVisitor[TType],
    DeclNodeVisitor[TDecl],
    StmtNodeVisitor[TStmt],
    ExprNodeVisitor[TExpr],
    Protocol
):
    """A master visitor pattern interface for coordinating cross-domain resolved node traversals."""
    pass

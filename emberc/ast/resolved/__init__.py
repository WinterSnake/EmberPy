##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## AST: Resolved                 ##
##-------------------------------##

## Imports
from .declarations import (
    DeclNode,
    DeclUnitNode,
    DeclSequenceNode,
    DeclVariableNode,
)
from .expressions import (
    ExprNode,
    ExprAssignNode,
    ExprBinaryNode,
    ExprIntegerNode,
    ExprVariableNode,
)
from .statements import (
    StmtNode,
    StmtEmptyNode,
    StmtExpressionNode,
)
from .types import (
    TypeNode,
    TypePending,
    TypePrimitive,
)

## Constants
__all__ = (
    "ResolvedNode",
    # -Types
    "TypeNode",
    "TypePending",
    "TypePrimitive",
    # -Declarations
    "DeclNode",
    "DeclUnitNode",
    "DeclSequenceNode",
    "DeclVariableNode",
    # -Statements
    "StmtNode",
    "StmtEmptyNode",
    "StmtExpressionNode",
    # -Expressions
    "ExprNode",
    "ExprAssignNode",
    "ExprBinaryNode",
    "ExprIntegerNode",
    "ExprVariableNode",
)
type ResolvedNode = TypeNode | DeclNode | StmtNode | ExprNode

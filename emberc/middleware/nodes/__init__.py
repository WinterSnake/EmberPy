##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Middleware: Nodes             ##
##-------------------------------##

## Imports
from .node import NodeBase
from .decl import NodeDecl
from .decl_unit import NodeDeclUnit
from .decl_variable import NodeDeclVariable
from .expr import NodeExpr
from .expr_assignment import NodeExprAssignment
from .expr_binary import NodeExprBinary
from .expr_group import NodeExprGroup
from .expr_literal import LITERAL_VALUE, NodeExprLiteral
from .expr_unary import NodeExprUnary
from .expr_variable import NodeExprVariable
from .stmt import NodeStmt
from .stmt_expression import NodeStmtExpression
from .typed import NodeType, NodeTypeBuiltin, NodeTypeIdentifier

## Constants
type LITERAL_TYPE = NodeType | NodeExpr
__all__ = (
    "LITERAL_TYPE", "LITERAL_VALUE",
    "NodeBase", "NodeType", "NodeDecl", "NodeStmt", "NodeExpr",
    "NodeTypeBuiltin", "NodeTypeIdentifier",
    "NodeDeclUnit", "NodeDeclVariable",
    "NodeStmtExpression",
    "NodeExprAssignment", "NodeExprGroup", "NodeExprBinary", "NodeExprUnary",
    "NodeExprVariable", "NodeExprLiteral",
)

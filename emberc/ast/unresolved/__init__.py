##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## AST: Unresolved               ##
##-------------------------------##

## Imports
from .assignment import UnresolvedAssignmentNode
from .binary import UnresolvedBinaryNode
from .block import UnresolvedBlockNode
from .conditional import UnresolvedConditionalNode, UnresolvedSwitchNode
from .enum import ENUM_ENTRY_TYPES, UnresolvedEnumNode
from .expression import UnresolvedExprNode, UnresolvedEmptyNode
from .function import UnresolvedFunctionNode, UnresolvedReturnNode
from .group import UnresolvedGroupNode
from .literal import (
    AST_LITERAL_TYPES,
    UnresolvedArrayNode,
    UnresolvedLiteralNode,
    UnresolvedIdentifierNode
)
from .loops import (
    UnresolvedWhileNode,
    UnresolvedDoNode,
    UnresolvedForNode,
    UnresolvedFlowNode,
)
from .node import UnresolvedNode, UnresolvedUnitNode
from .struct import STRUCT_MEMBER_TYPES, UnresolvedStructNode
from .types import UnresolvedTypeNode, UnresolvedModifierNode
from .unary import (
    UnresolvedUnaryPrefixNode,
    UnresolvedUnaryPostfixNode,
    UnresolvedAccessNode,
)
from .variable import UnresolvedVariableNode
from .visitor import UnresolvedNodeVisitor

## Constants
__all__ = (
    # -Core
    "AST_LITERAL_TYPES",
    "STRUCT_MEMBER_TYPES",
    "ENUM_ENTRY_TYPES",
    "UnresolvedNode",
    "UnresolvedNodeVisitor",
    "UnresolvedUnitNode",
    # -Types
    "UnresolvedTypeNode",
    "UnresolvedModifierNode",
    # -Declarations
    "UnresolvedStructNode",
    "UnresolvedFunctionNode",
    "UnresolvedEnumNode",
    "UnresolvedVariableNode",
    # -Statements
    "UnresolvedBlockNode",
    "UnresolvedConditionalNode",
    "UnresolvedSwitchNode",
    "UnresolvedWhileNode",
    "UnresolvedDoNode",
    "UnresolvedForNode",
    "UnresolvedFlowNode",
    "UnresolvedReturnNode",
    "UnresolvedExprNode",
    # -Expressions
    "UnresolvedGroupNode",
    "UnresolvedAssignmentNode",
    "UnresolvedBinaryNode",
    "UnresolvedUnaryPrefixNode",
    "UnresolvedUnaryPostfixNode",
    "UnresolvedAccessNode",
    "UnresolvedArrayNode",
    "UnresolvedLiteralNode",
    "UnresolvedIdentifierNode",
    "UnresolvedEmptyNode",
)

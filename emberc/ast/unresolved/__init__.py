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
from .expression import (
    UnresolvedExprNode,
    UnresolvedDeferNode,
    UnresolvedEmptyNode
)
from .function import UnresolvedFunctionNode, UnresolvedReturnNode
from .group import UnresolvedGroupNode
from .literal import (
    AST_LITERAL_TYPES,
    UnresolvedObjectNode,
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
    "UnresolvedNullVisitorMixin",
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
    "UnresolvedDeferNode",
    "UnresolvedExprNode",
    # -Expressions
    "UnresolvedGroupNode",
    "UnresolvedAssignmentNode",
    "UnresolvedBinaryNode",
    "UnresolvedUnaryPrefixNode",
    "UnresolvedUnaryPostfixNode",
    "UnresolvedAccessNode",
    "UnresolvedObjectNode",
    "UnresolvedArrayNode",
    "UnresolvedLiteralNode",
    "UnresolvedIdentifierNode",
    "UnresolvedEmptyNode",
)


## Classes
class UnresolvedNullVisitorMixin[T](UnresolvedNodeVisitor[T | None]):
    # -Instance Methods: Visitor
    def visit_unit(self, node: UnresolvedUnitNode) -> T | None:
        return None
    def visit_type(self, node: UnresolvedTypeNode) -> T | None:
        return None
    def visit_modifier(self, node: UnresolvedModifierNode) -> T | None:
        return None
    def visit_decl_struct(self, node: UnresolvedStructNode) -> T | None:
        return None
    def visit_decl_function(self, node: UnresolvedFunctionNode) -> T | None:
        return None
    def visit_decl_enum(self, node: UnresolvedEnumNode) -> T | None:
        return None
    def visit_decl_variable(self, node: UnresolvedVariableNode) -> T | None:
        return None
    def visit_stmt_block(self, node: UnresolvedBlockNode) -> T | None:
        return None
    def visit_stmt_conditional(self, node: UnresolvedConditionalNode) -> T | None:
        return None
    def visit_stmt_switch(self, node: UnresolvedSwitchNode) -> T | None:
        return None
    def visit_stmt_while(self, node: UnresolvedWhileNode) -> T | None:
        return None
    def visit_stmt_do(self, node: UnresolvedDoNode) -> T | None:
        return None
    def visit_stmt_for(self, node: UnresolvedForNode) -> T | None:
        return None
    def visit_stmt_flow(self, node: UnresolvedFlowNode) -> T | None:
        return None
    def visit_stmt_return(self, node: UnresolvedReturnNode) -> T | None:
        return None
    def visit_stmt_defer(self, node: UnresolvedDeferNode) -> T | None:
        return None
    def visit_stmt_expression(self, node: UnresolvedExprNode) -> T | None:
        return None
    def visit_expr_group(self, node: UnresolvedGroupNode) -> T | None:
        return None
    def visit_expr_assignment(self, node: UnresolvedAssignmentNode) -> T | None:
        return None
    def visit_expr_binary(self, node: UnresolvedBinaryNode) -> T | None:
        return None
    def visit_expr_unary_prefix(self, node: UnresolvedUnaryPrefixNode) -> T | None:
        return None
    def visit_expr_unary_postfix(self, node: UnresolvedUnaryPostfixNode) -> T | None:
        return None
    def visit_expr_access(self, node: UnresolvedAccessNode) -> T | None:
        return None
    def visit_expr_object(self, node: UnresolvedObjectNode) -> T | None:
        return None
    def visit_expr_array(self, node: UnresolvedArrayNode) -> T | None:
        return None
    def visit_expr_literal(self, node: UnresolvedLiteralNode) -> T | None:
        return None
    def visit_expr_identifier(self, node: UnresolvedIdentifierNode) -> T | None:
        return None
    def visit_expr_empty(self, node: UnresolvedEmptyNode) -> T | None:
        return None

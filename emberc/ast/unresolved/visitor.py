##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Visitor      ##
##-------------------------------##

## Imports
from abc import ABC, abstractmethod
from .assignment import UnresolvedAssignmentNode
from .binary import UnresolvedBinaryNode
from .block import UnresolvedBlockNode
from .conditional import UnresolvedConditionalNode
from .enum import UnresolvedEnumNode
from .expression import UnresolvedExprNode, UnresolvedEmptyNode
from .function import UnresolvedFunctionNode, UnresolvedReturnNode
from .group import UnresolvedGroupNode
from .literal import (
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
from .types import UnresolvedTypeNode, UnresolvedModifierNode
from .unary import (
    UnresolvedUnaryPrefixNode,
    UnresolvedUnaryPostfixNode,
    UnresolvedAccessNode,
)
from .variable import UnresolvedVariableNode


## Classes
class UnresolvedNodeVisitor[TReturn](ABC):
    """
    Unresolved AST Visitor

    A traversal interface for walking an unresolved AST tree.
    """
    # -Instance Methods
    def visit(self, node: UnresolvedNode) -> TReturn:
        match node:
            # -Types
            case UnresolvedTypeNode():
                return self.visit_type(node)
            case UnresolvedModifierNode():
                return self.visit_modifier(node)
            # -Declarations
            case UnresolvedUnitNode():
                return self.visit_decl_unit(node)
            case UnresolvedFunctionNode():
                return self.visit_decl_function(node)
            case UnresolvedEnumNode():
                return self.visit_decl_enum(node)
            case UnresolvedVariableNode():
                return self.visit_decl_variable(node)
            # -Statements
            case UnresolvedBlockNode():
                return self.visit_stmt_block(node)
            case UnresolvedConditionalNode():
                return self.visit_stmt_conditional(node)
            case UnresolvedWhileNode():
                return self.visit_stmt_while(node)
            case UnresolvedDoNode():
                return self.visit_stmt_do(node)
            case UnresolvedForNode():
                return self.visit_stmt_for(node)
            case UnresolvedFlowNode():
                return self.visit_stmt_flow(node)
            case UnresolvedReturnNode():
                return self.visit_stmt_return(node)
            case UnresolvedExprNode():
                return self.visit_stmt_expression(node)
            # -Expressions
            case UnresolvedGroupNode():
                return self.visit_expr_group(node)
            case UnresolvedAssignmentNode():
                return self.visit_expr_assignment(node)
            case UnresolvedBinaryNode():
                return self.visit_expr_binary(node)
            case UnresolvedUnaryPrefixNode():
                return self.visit_expr_unary_prefix(node)
            case UnresolvedUnaryPostfixNode():
                return self.visit_expr_unary_postfix(node)
            case UnresolvedAccessNode():
                return self.visit_expr_access(node)
            case UnresolvedArrayNode():
                return self.visit_expr_array(node)
            case UnresolvedLiteralNode():
                return self.visit_expr_literal(node)
            case UnresolvedIdentifierNode():
                return self.visit_expr_identifier(node)
            case UnresolvedEmptyNode():
                return self.visit_expr_empty(node)
            case _:
                raise RuntimeError("Unhandled node type", node, "in UnresolvedNodeVisitor")

    @abstractmethod
    def visit_type(self, node: UnresolvedTypeNode) -> TReturn: ...
    @abstractmethod
    def visit_modifier(self, node: UnresolvedModifierNode) -> TReturn: ...
    @abstractmethod
    def visit_decl_unit(self, node: UnresolvedUnitNode) -> TReturn: ...
    @abstractmethod
    def visit_decl_function(self, node: UnresolvedFunctionNode) -> TReturn: ...
    @abstractmethod
    def visit_decl_enum(self, node: UnresolvedEnumNode) -> TReturn: ...
    @abstractmethod
    def visit_decl_variable(self, node: UnresolvedVariableNode) -> TReturn: ...
    @abstractmethod
    def visit_stmt_block(self, node: UnresolvedBlockNode) -> TReturn: ...
    @abstractmethod
    def visit_stmt_conditional(self, node: UnresolvedConditionalNode) -> TReturn: ...
    @abstractmethod
    def visit_stmt_while(self, node: UnresolvedWhileNode) -> TReturn: ...
    @abstractmethod
    def visit_stmt_do(self, node: UnresolvedDoNode) -> TReturn: ...
    @abstractmethod
    def visit_stmt_for(self, node: UnresolvedForNode) -> TReturn: ...
    @abstractmethod
    def visit_stmt_flow(self, node: UnresolvedFlowNode) -> TReturn: ...
    @abstractmethod
    def visit_stmt_return(self, node: UnresolvedReturnNode) -> TReturn: ...
    @abstractmethod
    def visit_stmt_expression(self, node: UnresolvedExprNode) -> TReturn: ...
    @abstractmethod
    def visit_expr_group(self, node: UnresolvedGroupNode) -> TReturn: ...
    @abstractmethod
    def visit_expr_assignment(self, node: UnresolvedAssignmentNode) -> TReturn: ...
    @abstractmethod
    def visit_expr_binary(self, node: UnresolvedBinaryNode) -> TReturn: ...
    @abstractmethod
    def visit_expr_unary_prefix(self, node: UnresolvedUnaryPrefixNode) -> TReturn: ...
    @abstractmethod
    def visit_expr_unary_postfix(self, node: UnresolvedUnaryPostfixNode) -> TReturn: ...
    @abstractmethod
    def visit_expr_access(self, node: UnresolvedAccessNode) -> TReturn: ...
    @abstractmethod
    def visit_expr_array(self, node: UnresolvedArrayNode) -> TReturn: ...
    @abstractmethod
    def visit_expr_literal(self, node: UnresolvedLiteralNode) -> TReturn: ...
    @abstractmethod
    def visit_expr_identifier(self, node: UnresolvedIdentifierNode) -> TReturn: ...
    @abstractmethod
    def visit_expr_empty(self, node: UnresolvedEmptyNode) -> TReturn: ...

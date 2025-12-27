##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Visitor      ##
##-------------------------------##

## Imports
from abc import ABC, abstractmethod
from .assign import UnresolvedAssignNode
from .binary import UnresolvedBinaryNode
from .declaration import (
    UnresolvedDeclFunctionNode,
    UnresolvedDeclVariableNode,
)
from .group import UnresolvedGroupNode
from .identifier import UnresolvedIdentifierNode
from .literal import (
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


## Classes
class UnresolvedNodeVisitor[TReturn](ABC):
    """
    Ember AST Node: Unresolved Visitor

    A visitor for traversing through unresolved nodes in a single dispatch
    """

    # -Instance Methods
    @abstractmethod
    def run(self, ast: UnresolvedUnitNode) -> TReturn: ...
    def visit(self, node: UnresolvedNode) -> TReturn:
        match node:
            case UnresolvedTypeNode():
                return self.visit_type(node)
            case UnresolvedDeclFunctionNode():
                return self.visit_decl_function(node)
            case UnresolvedDeclVariableNode():
                return self.visit_decl_variable(node)
            case UnresolvedStmtEmptyNode():
                return self.visit_stmt_empty(node)
            case UnresolvedStmtBlockNode():
                return self.visit_stmt_block(node)
            case UnresolvedStmtConditionalNode():
                return self.visit_stmt_condition(node)
            case UnresolvedStmtLoopWhileNode():
                return self.visit_stmt_loop_while(node)
            case UnresolvedStmtLoopDoNode():
                return self.visit_stmt_loop_do(node)
            case UnresolvedStmtLoopForNode():
                return self.visit_stmt_loop_for(node)
            case UnresolvedStmtReturnNode():
                return self.visit_stmt_return(node)
            case UnresolvedStmtExpressionNode():
                return self.visit_stmt_expression(node)
            case UnresolvedExprEmptyNode():
                return self.visit_expr_empty(node)
            case UnresolvedAssignNode():
                return self.visit_assignment(node)
            case UnresolvedBinaryNode():
                return self.visit_binary(node)
            case UnresolvedUnaryModifierNode():
                return self.visit_unary_modifier(node)
            case UnresolvedUnaryPrefixNode():
                return self.visit_unary_prefix(node)
            case UnresolvedUnaryPostfixNode():
                return self.visit_unary_postfix(node)
            case UnresolvedGroupNode():
                return self.visit_group(node)
            case UnresolvedArrayNode():
                return self.visit_array(node)
            case UnresolvedLiteralNode():
                return self.visit_literal(node)
            case UnresolvedIdentifierNode():
                return self.visit_identifier(node)
            case _:
                raise RuntimeError("Unhandled node type", node, "in NodeVisitor")

    @abstractmethod
    def visit_type(self, node: UnresolvedTypeNode) -> TReturn: ...
    @abstractmethod
    def visit_decl_function(self, node: UnresolvedDeclFunctionNode) -> TReturn: ...
    @abstractmethod
    def visit_decl_variable(self, node: UnresolvedDeclVariableNode) -> TReturn: ...
    @abstractmethod
    def visit_stmt_empty(self, node: UnresolvedStmtEmptyNode) -> TReturn: ...
    @abstractmethod
    def visit_stmt_block(self, node: UnresolvedStmtBlockNode) -> TReturn: ...
    @abstractmethod
    def visit_stmt_condition(self, node: UnresolvedStmtConditionalNode) -> TReturn: ...
    @abstractmethod
    def visit_stmt_loop_while(self, node: UnresolvedStmtLoopWhileNode) -> TReturn: ...
    @abstractmethod
    def visit_stmt_loop_do(self, node: UnresolvedStmtLoopDoNode) -> TReturn: ...
    @abstractmethod
    def visit_stmt_loop_for(self, node: UnresolvedStmtLoopForNode) -> TReturn: ...
    @abstractmethod
    def visit_stmt_return(self, node: UnresolvedStmtReturnNode) -> TReturn: ...
    @abstractmethod
    def visit_stmt_expression(self, node: UnresolvedStmtExpressionNode) -> TReturn: ...
    @abstractmethod
    def visit_expr_empty(self, node: UnresolvedExprEmptyNode) -> TReturn: ...
    @abstractmethod
    def visit_assignment(self, node: UnresolvedAssignNode) -> TReturn: ...
    @abstractmethod
    def visit_binary(self, node: UnresolvedBinaryNode) -> TReturn: ...
    @abstractmethod
    def visit_unary_modifier(self, node: UnresolvedUnaryModifierNode) -> TReturn: ...
    @abstractmethod
    def visit_unary_prefix(self, node: UnresolvedUnaryPrefixNode) -> TReturn: ...
    @abstractmethod
    def visit_unary_postfix(self, node: UnresolvedUnaryPostfixNode) -> TReturn: ...
    @abstractmethod
    def visit_group(self, node: UnresolvedGroupNode) -> TReturn: ...
    @abstractmethod
    def visit_array(self, node: UnresolvedArrayNode) -> TReturn: ...
    @abstractmethod
    def visit_literal(self, node: UnresolvedLiteralNode) -> TReturn: ...
    @abstractmethod
    def visit_identifier(self, node: UnresolvedIdentifierNode) -> TReturn: ...

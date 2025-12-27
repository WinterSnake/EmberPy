##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolution: Global Resolution ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import TYPE_CHECKING
from .subscript_evaluator import SubscriptFinalizerVisitor
from .type_factory import TypeFactoryVisitor
from .variable_evaluator import VariableEvaluatorVisitor
from ...ast import (
    # -Unresolved
    UnresolvedUnitNode,
    UnresolvedNodeVisitor, UnresolvedDefaultVisitorMixin,
    # -Resolved
    NodeTypeFunction
)

if TYPE_CHECKING:
    from ..symbol_table import SymbolTable
    from ...ast import (
        # -Unresolved
        UnresolvedNode,
        UnresolvedDeclFunctionNode, UnresolvedDeclVariableNode,
        UnresolvedStmtBlockNode, UnresolvedStmtExpressionNode,
        UnresolvedStmtConditionalNode, UnresolvedStmtLoopWhileNode,
        UnresolvedStmtLoopDoNode, UnresolvedStmtLoopForNode,
        UnresolvedStmtReturnNode,
        UnresolvedGroupNode, UnresolvedExprEmptyNode,
        UnresolvedAssignNode, UnresolvedBinaryNode,
        UnresolvedUnaryPrefixNode, UnresolvedUnaryPostfixNode,
        UnresolvedIdentifierNode, UnresolvedLiteralNode, UnresolvedArrayNode,
    )


## Classes
class LocalBindingVisitor(
    UnresolvedDefaultVisitorMixin[None],
    UnresolvedNodeVisitor[None]
):
    """
    Local Binding

    Traverses the AST tree and binds every declaration
    by their type and name to the symbol table at the local scope
    and walks all expressions to bind atoms to scope
    """

    # -Constructor
    def __init__(self, symbol_table: SymbolTable) -> None:
        self._symbol_table = symbol_table
        self._mapped_initializers: dict[int, UnresolvedNode] = {}
        self._subscript_eval = SubscriptFinalizerVisitor(
            symbol_table, self._mapped_initializers
        )
        self._type_factory = TypeFactoryVisitor(symbol_table)
        self._variable_eval = VariableEvaluatorVisitor()

    # -Instance Methods
    def run(self, ast: UnresolvedUnitNode) -> None:
        for child in ast.children:
            self.visit(child)

    def visit_decl_function(self, node: UnresolvedDeclFunctionNode) -> None:
        if self._symbol_table.scope_depth > 0:
            assert False, "TODO: Error handling"
        symbol = self._symbol_table.get(node.id)
        symbol.type.bind(self)
        symbol._type = symbol.type.accept(self._subscript_eval)
        assert isinstance(symbol.type, NodeTypeFunction), "TODO: Error handling"
        parameter_types = symbol.type.parameter_types
        self._symbol_table.push()
        for parameter_type, parameter in zip(parameter_types, node.parameters):
            _id = self._symbol_table.add_parameter(parameter.name, parameter_type)
            assert _id is not None, "TODO: Error handling"
            parameter.id = _id
            if parameter.has_initializer:
                self.visit(parameter.initializer)
        assert self._variable_eval.validate_parameters(node.parameters), "TODO: Error handling"
        self.visit(node.body)
        self._symbol_table.pop()

    def visit_decl_variable(self, node: UnresolvedDeclVariableNode) -> None:
        local_scope = self._symbol_table.scope_depth > 0
        _type = self._type_factory.visit(node.type) if local_scope else None
        for entry in node.entries:
            if local_scope:
                assert _type is not None, "TODO: Error handling"
                _id = self._symbol_table.add_variable(entry.name, _type)
                assert _id is not None, "TODO: Error handling"
                entry.id = _id
            if entry.has_initializer:
                self._mapped_initializers[entry.id] = entry.initializer
                self.visit(entry.initializer)
                self._subscript_eval.current_initializer = entry.initializer
            symbol = self._symbol_table.get(entry.id)
            symbol.type.bind(self)
            symbol._type = symbol.type.accept(self._subscript_eval)
            self._subscript_eval.reset_initializer()
        assert self._variable_eval.validate_variable(node), "TODO: Error handling"

    def visit_stmt_block(self, node: UnresolvedStmtBlockNode) -> None:
        self._symbol_table.push()
        for element in node.elements:
            self.visit(element)
        self._symbol_table.pop()

    def visit_stmt_condition(self, node: UnresolvedStmtConditionalNode) -> None:
        self.visit(node.condition)
        self.visit(node.if_branch)
        if node.has_else_branch:
            self.visit(node.else_branch)

    def visit_stmt_loop_while(self, node: UnresolvedStmtLoopWhileNode) -> None:
        self.visit(node.condition)
        self.visit(node.body)

    def visit_stmt_loop_do(self, node: UnresolvedStmtLoopDoNode) -> None:
        self.visit(node.condition)
        self.visit(node.body)

    def visit_stmt_loop_for(self, node: UnresolvedStmtLoopForNode) -> None:
        if node.has_initializer:
            self.visit(node.initializer)
        self.visit(node.condition)
        if node.has_increment:
            self.visit(node.increment)
        self.visit(node.body)

    def visit_stmt_return(self, node: UnresolvedStmtReturnNode) -> None:
        if node.has_value:
            self.visit(node.value)

    def visit_stmt_expression(self, node: UnresolvedStmtExpressionNode) -> None:
        self.visit(node.expression)

    def visit_assignment(self, node: UnresolvedAssignNode) -> None:
        self.visit(node.l_value)
        self.visit(node.r_value)

    def visit_binary(self, node: UnresolvedBinaryNode) -> None:
        self.visit(node.lhs)
        self.visit(node.rhs)

    def visit_unary_prefix(self, node: UnresolvedUnaryPrefixNode) -> None:
        self.visit(node.operand)

    def visit_unary_postfix(self, node: UnresolvedUnaryPostfixNode) -> None:
        self.visit(node.head)

    def visit_group(self, node: UnresolvedGroupNode) -> None:
        self.visit(node.inner)
        if node.has_target:
            self.visit(node.target)

    def visit_array(self, node: UnresolvedArrayNode) -> None:
        for value in node.values:
            self.visit(value)

    def visit_identifier(self, node: UnresolvedIdentifierNode) -> None:
        _id = self._symbol_table.find(node.name)
        assert _id is not None, "TODO: Error handling"
        node.id = _id

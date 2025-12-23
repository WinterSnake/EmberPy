##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Pass: Binding                 ##
##-------------------------------##

## Imports
from ..nodes import (
    NODE_TYPES,
    NodeType, NodeDecl, NodeStmt, NodeExpr,
    NodeTypeBuiltin, NodeTypeIdentifier,
    NodeDeclUnit, NodeDeclFunction, NodeDeclVariable,
    NodeStmtBlock, NodeStmtConditional, NodeStmtLoop,
    NodeStmtReturn, NodeStmtExpression,
    NodeExprAssignment, NodeExprGroup, NodeExprBinary, NodeExprUnary,
    NodeExprCall, NodeExprVariable, NodeExprLiteral,
)
from ..symbol_table import Symbol, SymbolTable
from ..visitor import NodeVisitor, null_type_visitor


## Classes
class NodeBindingPass(NodeVisitor):
    """
    Ember Pass: Binding

    Handles scoping of symbol table and registers parameters/local variables.
    Additionally modifies expr var types as TypeIdentifier
    """

    # -Constructor
    def __init__(self, symbol_table: SymbolTable) -> None:
        super().__init__(null_type_visitor, self, self, self)
        self._symbol_table = symbol_table

    # -Instance Methods
    def visit_type_meta(self, node: NODE_TYPES) -> NodeType:
        match node:
            case NodeTypeBuiltin():
                return self.visit_type_builtin(node, self)
            case NodeExprVariable():
                return self.visit_type_variable(node, self)
            case _:
                raise RuntimeError(f"Unknown type in resolution.visit_type({node})")

    def visit_type_builtin(self, node: NodeTypeBuiltin, manager: NodeVisitor) -> NodeType:
        return node

    def visit_type_variable(self, node: NodeExprVariable, manager: NodeVisitor) -> NodeType:
        idx = self._symbol_table.find(node.name)
        # -TODO: Error handling
        assert idx is not None
        return NodeTypeIdentifier(node.location, idx)

    def visit_decl_unit(self, node: NodeDeclUnit, manager: NodeVisitor) -> NodeDecl:
        for decl in node.body:
            self.visit(decl)
        return node

    def visit_decl_function(self, node: NodeDeclFunction, manager: NodeVisitor) -> None:
        # -Internal Functions
        def _visit_internals() -> None:
            self._symbol_table.push()
            for parameter in node.parameters:
                self.visit_declaration(parameter)
            self.visit_statement(node.body)
            self._symbol_table.pop()

        # -Body
        if self._symbol_table.scope_depth == 0:
            _visit_internals()
        else:
            raise RuntimeError("Nested functions are not supported yet in binding")

    def visit_decl_variable(self, node: NodeDeclVariable, manager: NodeVisitor) -> None:
        # -Internal Functions
        def _visit_internals() -> None:
            if node.has_initializer:
                self.visit_expression(node.initializer)

        # -Body
        if self._symbol_table.scope_depth == 0:
            _visit_internals()
            return
        node._type = self.visit_type_meta(node._type)
        idx = self._symbol_table.add(node.name, Symbol.Kind.Variable, node.type)
        # -TODO: Error handling
        assert idx is not None
        node._id = idx
        _visit_internals()

    def visit_stmt_block(self, node: NodeStmtBlock, manager: NodeVisitor) -> None:
        self._symbol_table.push()
        for elem in node.body:
            self.visit(elem)
        self._symbol_table.pop()

    def visit_stmt_conditional(self, node: NodeStmtConditional, manager: NodeVisitor) -> None:
        self.visit_expression(node.condition)
        self.visit_statement(node.then_branch)
        if node.has_else_branch:
            self.visit_statement(node.else_branch)

    def visit_stmt_loop(self, node: NodeStmtLoop, manager: NodeVisitor) -> None:
        self.visit_expression(node.condition)
        self.visit_statement(node.body)

    def visit_stmt_return(self, node: NodeStmtReturn, manager: NodeVisitor) -> None:
        if node.has_value:
            self.visit_expression(node.value)

    def visit_stmt_expression(self, node: NodeStmtExpression, manager: NodeVisitor) -> None:
        if not node.is_empty:
            self.visit_expression(node.expression)

    def visit_expr_assignment(self, node: NodeExprAssignment, manager: NodeVisitor) -> None:
        self.visit_expression(node.l_value)
        self.visit_expression(node.r_value)

    def visit_expr_group(self, node: NodeExprGroup, manager: NodeVisitor) -> None:
        self.visit_expression(node.expression)

    def visit_expr_binary(self, node: NodeExprBinary, manager: NodeVisitor) -> None:
        self.visit_expression(node.lhs)
        self.visit_expression(node.rhs)

    def visit_expr_unary(self, node: NodeExprUnary, manager: NodeVisitor) -> None:
        self.visit_expression(node.expression)

    def visit_expr_call(self, node: NodeExprCall, manager: NodeVisitor) -> None:
        self.visit_expression(node.callee)
        for argument in node.arguments:
            self.visit_expression(argument)

    def visit_expr_literal(self, node: NodeExprLiteral, manager: NodeVisitor) -> None:
        return

    def visit_expr_variable(self, node: NodeExprVariable, manager: NodeVisitor) -> None:
        if node.state != NodeExprVariable.State.Raw:
            return
        idx = self._symbol_table.find(node.name)
        # -TODO: Error handling
        assert idx is not None
        node.bind(idx)

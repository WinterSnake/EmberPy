##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Pass: Resolution              ##
##-------------------------------##

## Imports
from typing import cast
from ..nodes import (
    NODE_TYPES,
    NodeType, NodeDecl,
    NodeTypeBuiltin, NodeTypeIdentifier,
    NodeDeclUnit, NodeDeclFunction, NodeDeclVariable,
    NodeExprVariable,
)
from ..symbol_table import Symbol, SymbolTable
from ..visitor import (
    NodeVisitor,
    null_type_visitor, null_stmt_visitor, null_expr_visitor
)


## Classes
class NodeResolutionPass(NodeVisitor):
    """
    Ember Pass: Resolution

    Registers global functions and variables to the symbol table
    Additionally modifies expr var types as TypeIdentifier
    """

    # -Constructor
    def __init__(self, symbol_table: SymbolTable) -> None:
        super().__init__(null_type_visitor, self, null_stmt_visitor, null_expr_visitor)
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
        node._type = self.visit_type_meta(node._type)
        idx = self._symbol_table.add(node.name, Symbol.Kind.Function, node.type)
        # -TODO: Error handling
        assert idx is not None
        node._id = idx
    
    def visit_decl_variable(self, node: NodeDeclVariable, manager: NodeVisitor) -> None:
        node._type = self.visit_type_meta(node._type)
        idx = self._symbol_table.add(node.name, Symbol.Kind.Variable, node.type)
        # -TODO: Error handling
        assert idx is not None
        node._id = idx

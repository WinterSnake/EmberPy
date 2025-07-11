##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node::Statement - Var Decl    ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import Any
from .core import Node, NodeExpr
from .visitor import NodeVisitor
from ...location import Location


## Classes
class NodeStmtDeclVar(Node):
    """
    Ember Statement Node: Variable Declaration
    Represents a statement for a variable declaration node
    """

    # -Constructor
    def __init__(self, _id: str, initializer: NodeExpr | None) -> None:
        self.id: str = _id
        self.initializer: NodeExpr | None = initializer

    # -Dunder Methods
    def __str__(self) -> str:
        _str = f"Id({self.id})"
        if self.initializer:
            _str += f" = {self.initializer}"
        return _str

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_statement_declaration_variable(self)

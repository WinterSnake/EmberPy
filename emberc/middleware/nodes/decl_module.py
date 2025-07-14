##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: DeclModule              ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Sequence
from typing import Any
from .core import Node, NodeContainer
from .visitor import NodeVisitor


## Classes
class NodeDeclModule(NodeContainer):
    """
    Ember Node: Declaration :: Module
    Represents an AST node of an entire module
    """

    # -Constructor
    def __init__(self, nodes: Sequence[Node]) -> None:
        super().__init__(nodes)

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_declaration_module(self)

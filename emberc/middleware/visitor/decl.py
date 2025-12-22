##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Visitor: Declaration          ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import TYPE_CHECKING, Protocol
from ..nodes import (
    NodeDeclUnit, NodeDeclVariable
)

if TYPE_CHECKING:
    from .visitor import NodeVisitor

## Classes
class NodeDeclVisitor[TReturn](Protocol):
    """
    Node Visitor : Declaration

    The node visitor for managing declaration typed nodes
    """

    # -Instance Methods
    def visit_decl_unit(self, node: NodeDeclUnit, manager: NodeVisitor) -> TReturn: ...
    def visit_decl_variable(self, node: NodeDeclVariable, manager: NodeVisitor) -> TReturn: ...

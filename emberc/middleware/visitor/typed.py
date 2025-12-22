##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Visitor: Typed                ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import TYPE_CHECKING, Protocol
from ..nodes import NodeTypeBuiltin, NodeTypeIdentifier

if TYPE_CHECKING:
    from .visitor import NodeVisitor


## Classes
class NodeTypeVisitor[TReturn](Protocol):
    """
    Node Visitor : Type

    The node visitor for managing typed nodes
    """

    # -Instance Methods
    def visit_type_builtin(self, node: NodeTypeBuiltin, manager: NodeVisitor) -> TReturn: ...
    def visit_type_custom(self, node: NodeTypeIdentifier, manager: NodeVisitor) -> TReturn: ...

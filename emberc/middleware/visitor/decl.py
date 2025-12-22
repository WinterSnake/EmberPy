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
    NodeDeclUnit
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
    def visit_unit(self, node: NodeDeclUnit, manager: NodeVisitor) -> TReturn: ...

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Declaration Unit        ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Collection
from typing import TYPE_CHECKING
from .node import NodeBase
from .decl import NodeDecl
from ...location import Location

if TYPE_CHECKING:
    from ..visitor import NodeVisitor, NodeDeclVisitor


## Classes
class NodeDeclUnit(NodeDecl):
    """
    Ember Declaration Node : Unit
    Represents an AST node of a compilation unit
    """

    # -Constructor
    def __init__(self, body: Collection[NodeBase]) -> None:
        self.body: Collection[NodeBase] = body

    # -Instance Methods
    def accept[T](self, visitor: NodeDeclVisitor[T], manager: NodeVisitor) -> T:
        return visitor.visit_decl_unit(self, manager)

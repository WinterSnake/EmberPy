##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Statement Expression    ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Collection
from typing import TYPE_CHECKING
from .node import NodeBase
from .stmt import NodeStmt
from ...location import Location

if TYPE_CHECKING:
    from ..visitor import NodeVisitor, NodeStmtVisitor


## Classes
class NodeStmtBlock(NodeStmt):
    """
    Ember Statement Node : Block
    Represents an AST node of a block of statements
    """

    # -Constructor
    def __init__(self, location: Location, body: Collection[NodeBase]) -> None:
        super().__init__(location)
        self.body: Collection[NodeBase] = body

    # -Dunder Methods
    def __str__(self) -> str:
        _str = "{\n"
        for node in self.body:
            _str += f"\t{node}\n"
        return _str + '}'

    # -Instance Methods
    def accept[T](self, visitor: NodeStmtVisitor[T], manager: NodeVisitor) -> T:
        return visitor.visit_block(self, manager)

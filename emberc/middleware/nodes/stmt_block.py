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
from .decl_variable import NodeDeclVariable
from .stmt import NodeStmt
from ...location import Location

if TYPE_CHECKING:
    from ..visitor import NodeVisitor, NodeStmtVisitor

## Constants
type BLOCK_TYPES = NodeStmt | NodeDeclVariable


## Classes
class NodeStmtBlock(NodeStmt):
    """
    Ember Statement Node : Block
    Represents an AST node of a block of statements
    """

    # -Constructor
    def __init__(self, location: Location, body: Collection[BLOCK_TYPES]) -> None:
        super().__init__(location)
        self.body: Collection[BLOCK_TYPES] = body

    # -Instance Methods
    def accept[T](self, visitor: NodeStmtVisitor[T], manager: NodeVisitor) -> T:
        return visitor.visit_stmt_block(self, manager)

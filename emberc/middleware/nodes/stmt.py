##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Statement               ##
##-------------------------------##

## Imports
from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING
from .node import NodeBase

if TYPE_CHECKING:
    from ..visitor import NodeVisitor, NodeStmtVisitor


## Classes
class NodeStmt(NodeBase):
    """
    Ember Statement Node
    Represents an AST node of a statement
    """

    # -Instance Methods
    @abstractmethod
    def accept[T](self, visitor: NodeStmtVisitor[T], manager: NodeVisitor) -> T: ...

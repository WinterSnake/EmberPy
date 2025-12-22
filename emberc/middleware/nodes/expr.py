##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Expression              ##
##-------------------------------##

## Imports
from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING
from .node import NodeBase
from ...location import Location

if TYPE_CHECKING:
    from ..visitor import NodeVisitor, NodeExprVisitor


## Classes
class NodeExpr(NodeBase):
    """
    Ember Expression Node
    Represents an AST node of an expression
    """

    # -Constructor
    def __init__(self, location: Location) -> None:
        super().__init__(location)

    # -Instance Methods
    @abstractmethod
    def accept[T](self, visitor: NodeExprVisitor[T], manager: NodeVisitor) -> T: ...

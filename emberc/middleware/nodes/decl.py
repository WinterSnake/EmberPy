##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Declaration             ##
##-------------------------------##

## Imports
from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING
from .node import NodeBase
from ...location import Location

if TYPE_CHECKING:
    from ..visitor import NodeVisitor, NodeDeclVisitor


## Classes
class NodeDecl(NodeBase):
    """
    Ember Declaration Node
    Represents an AST node of a declaration
    """

    # -Constructor
    def __init__(self, location: Location) -> None:
        super().__init__(location)

    # -Instance Methods
    @abstractmethod
    def accept[T](self, visitor: NodeDeclVisitor[T], manager: NodeVisitor) -> T: ...

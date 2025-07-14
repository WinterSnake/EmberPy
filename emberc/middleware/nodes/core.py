##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node                          ##
##-------------------------------##

## Imports
from abc import ABC, abstractmethod
from typing import Any
from .visitor import NodeVisitor
from ...location import Location


## Classes
class Node(ABC):
    """
    Ember Node
    Base class for all AST nodes
    """

    # -Instance Methods
    @abstractmethod
    def accept(self, visitor: NodeVisitor) -> Any: ...


class NodeExpr(Node):
    """
    Ember Node: Expression
    Base class for expression nodes with location for error handling
    """

    # -Constructor
    def __init__(self, location: Location) -> None:
        self.location: Location = location

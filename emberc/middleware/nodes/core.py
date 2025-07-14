##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node                          ##
##-------------------------------##

## Imports
from abc import ABC, abstractmethod
from collections.abc import Sequence
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


class NodeContainer(Node):
    """
    Ember Node: Container
    Base class for nodes with an inner collection of nodes
    """

    # -Constructor
    def __init__(self, nodes: Sequence[Node]) -> None:
        self.nodes: Sequence[Node] = nodes


class NodeExpr(Node):
    """
    Ember Node: Expression
    Base class for expression nodes with location for error handling
    """

    # -Constructor
    def __init__(self, location: Location) -> None:
        self.location: Location = location

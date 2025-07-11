##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node                          ##
##-------------------------------##

## Imports
from abc import ABC, abstractmethod
from typing import Any, Sequence
from .visitor import NodeVisitor
from ...location import Location


## Classes
class Node(ABC):
    """
    Ember Node
    Base AST Node Type
    """

    # -Instance Methods
    @abstractmethod
    def accept(self, visitor: NodeVisitor) -> Any: ...


class NodeExpr(Node):
    """
    Ember Node: Expression
    Base AST Expression Node Type
    """

    # -Constructor
    def __init__(self, location: Location) -> None:
        self.location: Location = location


class NodeContainer(Node):
    """
    Ember Node: Container
    Represents an AST node with an inner body block
    """

    # -Constructor
    def __init__(self, body: Sequence[Node]) -> None:
        self.body: Sequence[Node] = body

    # -Dunder Methods
    def __str__(self) -> str:
        return '[' + ','.join(str(node) for node in self.body) + ']'


class NodeModule(NodeContainer):
    """
    Ember Node: Module
    Represents an AST node of a file (module)
    """

    # -Constructor
    def __init__(self, body: Sequence[Node]) -> None:
        super().__init__(body)

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_module(self)

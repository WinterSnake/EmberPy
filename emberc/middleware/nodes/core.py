##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node                          ##
##-------------------------------##

## Imports
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Sequence
from .visitor import NodeVisitor
from ...location import Location


## Classes
class Node(ABC):
    """
    Ember Node
    Represents a base node for AST generation
    """

    # -Instance Methods
    @abstractmethod
    def accept(self, visitor: NodeVisitor) -> Any: ...


class NodeExpr(Node):
    """
    Ember Node: Expression
    Represents a base expression node for AST generation
    """

    # -Constructor
    def __init__(self, location: Location) -> None:
        self.location: Location = location


class NodeModule(Node):
    """
    Ember Node: Module
    Represents a compilation unit and all nodes attached
    """

    # -Constructor
    def __init__(self, statements: Sequence[Node]) -> None:
        self.statements: Sequence[Node] = statements

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_module(self)

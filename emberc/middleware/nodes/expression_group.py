##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Group                   ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import Any
from .node import Node
from .visitor import NodeVisitor
from ...location import Location


## Classes
class NodeExprGroup(Node):
    """
    Ember Expression Node: Group
    Represents a group expression with its inner node
    """

    # -Constructor
    def __init__(
        self, location: Location, inner_node: Node
    ) -> None:
        super().__init__(location)
        self.inner_node: Node = inner_node

    # -Dunder Methods
    def __str__(self) -> str:
        return f"({self.inner_node})"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_group(self)

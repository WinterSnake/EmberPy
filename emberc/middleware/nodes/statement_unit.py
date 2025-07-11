##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Unit                    ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from pathlib import Path
from typing import Any, Sequence
from .node import Node
from .visitor import NodeVisitor
from ...location import Location


## Classes
class NodeStatementUnit(Node):
    """
    Ember Statement Node: Unit
    Represents a compilation unit and all nodes attached
    """

    # -Constructor
    def __init__(self, file: Path, nodes: Sequence[Node]) -> None:
        super().__init__(Location(file, (0, 0, 0)))
        self.nodes: Sequence[Node] = nodes

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_statement_unit(self)

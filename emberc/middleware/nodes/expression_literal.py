##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Literal                 ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import Any
from .node import Node
from .visitor import NodeVisitor
from ...location import Location


## Classes
class NodeExprLiteral(Node):
    """
    Ember Expression Node: Literal
    Represents a literal expression node
    """

    # -Constructor
    def __init__(
        self, location: Location, _type: NodeExprLiteral.Type, value: int
    ) -> None:
        super().__init__(location)
        self.type: NodeExprLiteral.Type = _type
        self.value: int = value

    # -Dunder Methods
    def __str__(self) -> str:
        return f"{self.type.name}({self.value})"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_literal(self)

    # -Sub-Classes
    class Type(IntEnum):
        ''''''
        Integer = auto()

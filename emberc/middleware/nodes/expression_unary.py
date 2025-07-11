##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Unary                   ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import Any
from .node import Node
from .visitor import NodeVisitor
from ...location import Location


## Functions
def _unary_type_to_str(_type: NodeExprUnary.Type) -> str:
    """
    """
    match _type:
        case NodeExprUnary.Type.Negative:
            return '-'


## Classes
class NodeExprUnary(Node):
    """
    """

    # -Constructor
    def __init__(
        self, location: Location, _type: NodeExprUnary.Type, node: Node
    ) -> None:
        super().__init__(location)
        self.type: NodeExprUnary.Type = _type
        self.node: Node = node

    # -Dunder Methods
    def __str__(self) -> str:
        return f"({self.node} {_unary_type_to_str(self.type)})"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_unary(self)

    # -Sub-Classes
    class Type(IntEnum):
        ''''''
        Negative = auto()

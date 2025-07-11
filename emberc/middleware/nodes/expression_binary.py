##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Binary                  ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import Any
from .node import Node
from .visitor import NodeVisitor
from ...location import Location


## Functions
def _binary_type_to_str(_type: NodeExprBinary.Type) -> str:
    """
    """
    match _type:
        case NodeExprBinary.Type.Add:
            return '+'
        case NodeExprBinary.Type.Sub:
            return '-'
        case NodeExprBinary.Type.Mul:
            return '*'
        case NodeExprBinary.Type.Div:
            return '/'
        case NodeExprBinary.Type.Mod:
            return '%'


## Classes
class NodeExprBinary(Node):
    """
    """

    # -Constructor
    def __init__(
        self, location: Location, _type: NodeExprBinary.Type,
        lhs: Node, rhs: Node
    ) -> None:
        super().__init__(location)
        self.type: NodeExprBinary.Type = _type
        self.lhs: Node = lhs
        self.rhs: Node = rhs

    # -Dunder Methods
    def __str__(self) -> str:
        return f"({self.lhs} {self.rhs} {_binary_type_to_str(self.type)})"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_binary(self)

    # -Sub-Classes
    class Type(IntEnum):
        ''''''
        Add = auto()
        Sub = auto()
        Mul = auto()
        Div = auto()
        Mod = auto()

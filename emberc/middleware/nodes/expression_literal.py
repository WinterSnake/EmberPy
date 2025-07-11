##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node::Expression - Literal    ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import Any
from .core import NodeExpr
from .visitor import NodeVisitor
from ...location import Location


## Classes
class NodeExprId(NodeExpr):
    """
    Ember Expression Node: Id
    Represents an id expression node for variables
    """
    # -Constructor
    def __init__(
        self, location: Location, _id: str
    ) -> None:
        super().__init__(location)
        self.id: str = _id

    # -Dunder Methods
    def __str__(self) -> str:
        return f"Id({self.id})"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_id(self)


class NodeExprLiteral(NodeExpr):
    """
    Ember Expression Node: Literal
    Represents a literal expression node
    """

    # -Constructor
    def __init__(
        self, location: Location, _type: NodeExprLiteral.Type, value: bool | int
    ) -> None:
        super().__init__(location)
        self.type: NodeExprLiteral.Type = _type
        self.value: bool | int = value

    # -Dunder Methods
    def __str__(self) -> str:
        return f"{self.type.name}({self.value})"

    # -Instance Methods
    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_expression_literal(self)

    # -Sub-Classes
    class Type(IntEnum):
        '''Literal Type'''
        Boolean = auto()
        Integer = auto()

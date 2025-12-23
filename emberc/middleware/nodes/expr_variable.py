##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Expression Variable     ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import TYPE_CHECKING
from .expr import NodeExpr
from ...location import Location

if TYPE_CHECKING:
    from ..visitor import NodeVisitor, NodeExprVisitor


## Classes
class NodeExprVariable(NodeExpr):
    """
    Ember Expression Node : Variable
    Represents an AST node of a variable expression
    """

    # -Constructor
    def __init__(self, location: Location, name: str) -> None:
        super().__init__(location)
        self._id: int | str = name
        self.state: NodeExprVariable.State = NodeExprVariable.State.Raw

    # -Instance Methods
    def accept[T](self, visitor: NodeExprVisitor[T], manager: NodeVisitor) -> T:
        return visitor.visit_expr_variable(self, manager)

    def bind(self, _id: int) -> None:
        self._id = _id
        self.state = NodeExprVariable.State.Bound

    # -Properties
    @property
    def id(self) -> int:
        assert isinstance(self._id, int)
        return self._id

    @property
    def name(self) -> str:
        assert isinstance(self._id, str)
        return self._id

    # -Sub-Classes
    class State(IntEnum):
        Raw = auto()
        Bound = auto()

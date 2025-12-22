##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Declaration Variable    ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Collection
from typing import TYPE_CHECKING
from .decl import NodeDecl
from .expr import NodeExpr
from .typed import NodeType
from ...location import Location

if TYPE_CHECKING:
    from ..visitor import NodeVisitor, NodeDeclVisitor
    from ...frontend import Token


## Classes
class NodeDeclVariable(NodeDecl):
    """
    Ember Declaration Node : Variable
    Represents an AST node of a variable declaration
    """

    # -Constructor
    def __init__(
        self, location: Location, _type: NodeType | NodeExpr, _id: str,
        initializer: NodeExpr | None
    ) -> None:
        super().__init__(location)
        self.id: str = _id
        self.type: NodeType | NodeExpr = _type
        self._initializer: NodeExpr | None = initializer

    # -Dunder Methods
    def __str__(self) -> str:
        _str = f"[{self.type}]({self.id}"
        if self._initializer is not None:
            _str += f" = {self.initializer}"
        return _str + ')'

    # -Instance Methods
    def accept[T](self, visitor: NodeDeclVisitor[T], manager: NodeVisitor) -> T:
        return visitor.visit_variable(self, manager)

    # -Properties
    @property
    def initializer(self) -> NodeExpr:
        assert self._initializer is not None
        return self._initializer

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
from .typed import NODE_TYPES, NodeType
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
        self, location: Location, _type: NODE_TYPES, name: str,
        initializer: NodeExpr | None
    ) -> None:
        super().__init__(location)
        self._id: int | str = name
        self._type: NODE_TYPES = _type
        self._initializer: NodeExpr | None = initializer

    # -Instance Methods
    def accept[T](self, visitor: NodeDeclVisitor[T], manager: NodeVisitor) -> T:
        return visitor.visit_decl_variable(self, manager)

    # -Properties
    @property
    def id(self) -> int:
        assert isinstance(self._id, int)
        return self._id

    @property
    def name(self) -> str:
        assert isinstance(self._id, str)
        return self._id

    @property
    def type(self) -> NodeType:
        assert isinstance(self._type, NodeType)
        return self._type

    @property
    def has_initializer(self) -> bool:
        return self._initializer is not None

    @property
    def initializer(self) -> NodeExpr:
        assert self._initializer is not None
        return self._initializer

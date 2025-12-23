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
from .decl_variable import NodeDeclVariable
from .stmt import NodeStmt
from .typed import NODE_TYPES, NodeType
from ...location import Location

if TYPE_CHECKING:
    from ..visitor import NodeVisitor, NodeDeclVisitor
    from ...frontend import Token


## Classes
class NodeDeclFunction(NodeDecl):
    """
    Ember Declaration Node : Function
    Represents an AST node of a function declaration
    """

    # -Constructor
    def __init__(
        self, location: Location, name: str, _type: NODE_TYPES,
        parameters: Collection[NodeDeclVariable], body: NodeStmt
    ) -> None:
        super().__init__(location)
        self._id: int | str = name
        self._type: NODE_TYPES = _type
        self.parameters: Collection[NodeDeclVariable] = parameters
        self.body: NodeStmt = body

    # -Instance Methods
    def accept[T](self, visitor: NodeDeclVisitor[T], manager: NodeVisitor) -> T:
        return visitor.visit_decl_function(self, manager)

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
    def parameter_count(self) -> int:
        return len(self.parameters)

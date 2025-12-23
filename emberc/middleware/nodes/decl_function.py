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
from .typed import NODE_TYPES
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
        self.id: int
        self.name: str = name
        self.type: NODE_TYPES = _type
        self.parameters: Collection[NodeDeclVariable] = parameters
        self.body: NodeStmt = body

    # -Instance Methods
    def accept[T](self, visitor: NodeDeclVisitor[T], manager: NodeVisitor) -> T:
        return visitor.visit_decl_function(self, manager)

    # -Properties
    @property
    def parameter_count(self) -> int:
        return len(self.parameters)

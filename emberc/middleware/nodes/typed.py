##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Typed [builtin+custom]  ##
##-------------------------------##

## Imports
from __future__ import annotations
from abc import abstractmethod
from enum import IntEnum, auto
from typing import TYPE_CHECKING
from .node import NodeBase
from ...location import Location

if TYPE_CHECKING:
    from ..visitor import NodeVisitor, NodeTypeVisitor


## Classes
class NodeType(NodeBase):
    """
    Ember Type Node
    Represents an AST node of typing
    """

    # -Instance Methods
    @abstractmethod
    def accept[T](self, visitor: NodeTypeVisitor[T], manager: NodeVisitor) -> T: ...


class NodeTypeBuiltin(NodeType):
    """
    Ember Type Node : Builtin
    Represents an AST node of builtin type
    """

    # -Constructor
    def __init__(self, location: Location, _type: NodeTypeBuiltin.Type) -> None:
        super().__init__(location)
        self.type: NodeTypeBuiltin.Type = _type

    # -Instance Methods
    def accept[T](self, visitor: NodeTypeVisitor[T], manager: NodeVisitor) -> T:
        return visitor.visit_type_builtin(self, manager)

    # -Sub-Classes
    class Type(IntEnum):
        # -Math
        Void = auto()
        Boolean = auto()
        Int8 = auto()
        Int16 = auto()
        Int32 = auto()
        Int64 = auto()
        UInt8 = auto()
        UInt16 = auto()
        UInt32 = auto()
        UInt64 = auto()


class NodeTypeIdentifier(NodeType):
    """
    Ember Type Node : Identifier
    Represents an AST node of custom type
    """

    # -Constructor
    def __init__(self, location: Location, _id: int) -> None:
        super().__init__(location)
        self.id: int = _id

    # -Instance Methods
    def accept[T](self, visitor: NodeTypeVisitor[T], manager: NodeVisitor) -> T:
        return visitor.visit_type_custom(self, manager)

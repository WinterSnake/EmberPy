##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolved Node: Type           ##
##-------------------------------##

## Imports
from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING, Any, TypeVar
from ..node import ResolvedNode

if TYPE_CHECKING:
    from .visitor import NodeTypeVisitor
    from ...unresolved import UnresolvedNodeVisitor

## Constants


## Classes
class NodeType(ResolvedNode):
    """
    Ember Resolved Node: Type

    A resolved typed node for storing type information
    """

    # -Instance Methods
    @abstractmethod
    def accept[T](self, visitor: NodeTypeVisitor[T]) -> T: ...
    @abstractmethod
    def bind[T](self, visitor: UnresolvedNodeVisitor[T]) -> None: ...

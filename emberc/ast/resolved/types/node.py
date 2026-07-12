##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type: Node                    ##
##-------------------------------##

## Imports
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, NoReturn

if TYPE_CHECKING:
    from . import TypeNodeVisitor


## Classes
@dataclass(frozen=True, slots=True)
class TypeNode(ABC):
    """The abstract base class for all resolved type nodes."""
    # -Instance Methods
    @abstractmethod
    def accept[T](self, visitor: TypeNodeVisitor[T]) -> T: ...


@dataclass(frozen=True, slots=True)
class TypePending(TypeNode):
    """
    Resolved Pending Type
    Represents a pending typed node for futher type analysis and refinement.
    """
    # -Instance Methods
    def accept[T](self, visitor: TypeNodeVisitor[T]) -> NoReturn:
        assert False, "Tried visiting a pending type node"

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type: Node                    ##
##-------------------------------##

## Imports
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Self

if TYPE_CHECKING:
    from . import TypeNodeVisitor


## Classes
@dataclass(frozen=True, slots=True)
class TypeNode(ABC):
    """
    An abstract base class representing a completely resolved type node within the type system.
    """
    # -Instance Methods
    @abstractmethod
    def accept[T](self, visitor: TypeNodeVisitor[T]) -> T: ...

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Statment: Node                ##
##-------------------------------##

## Imports
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, NoReturn

if TYPE_CHECKING:
    from . import StmtNodeVisitor


## Classes
@dataclass(slots=True)
class StmtNode(ABC):
    """The abstract base class for all resolved statement nodes."""
    # -Instance Methods
    @abstractmethod
    def accept[T](self, visitor: StmtNodeVisitor[T]) -> T: ...


@dataclass(slots=True)
class StmtEmptyNode(StmtNode):
    """
    Resolved Empty Statement
    Wraps an empty statement terminated by a semicolon.
    """
    # -Instance Methods
    def accept[T](self, visitor: StmtNodeVisitor[T]) -> NoReturn:
        assert False, "Tried visiting an empty statement node"

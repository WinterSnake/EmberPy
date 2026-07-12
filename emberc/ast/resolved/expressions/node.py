##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Expression: Node              ##
##-------------------------------##

## Imports
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from ..types import TypePending

if TYPE_CHECKING:
    from . import ExprNodeVisitor
    from ..types import TypeNode


## Classes
@dataclass(slots=True)
class ExprNode(ABC):
    """The abstract base class for all resolved expression nodes."""
    # -Instance Methods
    @abstractmethod
    def accept[T](self, visitor: ExprNodeVisitor[T]) -> T: ...

    # -Properties
    type: TypeNode = field(default=TypePending(), kw_only=True)

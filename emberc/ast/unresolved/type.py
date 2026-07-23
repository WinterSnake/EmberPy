##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Type         ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from . import UnresolvedNodeVisitor
    from ..common import PrimitiveType


## Classes
@dataclass(slots=True)
class UnresolvedTypeNode(UnresolvedNode):
    """Built-in type AST node."""
    # -Instance Methods
    def accept[R](self, visitor: UnresolvedNodeVisitor[R]) -> R:
        return visitor.visit_type(self)

    # -Properties
    kind: PrimitiveType

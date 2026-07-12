##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved AST: Types         ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from . import UnresolvedNodeVisitor


## Classes
@dataclass(slots=True)
class UnresolvedTypeNode(UnresolvedNode):
    """
    An AST node representing a type specification or primitive type expression.
    Encapsulates the specific kind of built-in data type.
    """
    # -Instance Methods
    def accept[T](self, visitor: UnresolvedNodeVisitor[T]) -> T:
        return visitor.visit_type(self)

    # -Properties
    kind: UnresolvedTypeNode.Kind

    # -Sub-Classes
    class Kind(IntEnum):
        Int32 = auto()

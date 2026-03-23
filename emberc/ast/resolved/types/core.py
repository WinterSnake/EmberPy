##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolved Node: Type           ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from ..node import ResolvedNode


## Classes
class TypeNode(ResolvedNode):
    """
    Resolved AST Node: Type

    A representation for typed nodes within the Ember language.
    """
    pass


@dataclass(frozen=True, slots=True)
class PendingTypeNode(TypeNode):
    """
    Resolved Type Node: Pending

    Represents a type whose concrete identity or memory constraints
    are currently unknown.
    """
    pass

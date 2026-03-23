##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type Node: Pointers           ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from .core import TypeNode


## Classes
@dataclass(slots=True)
class PointerTypeNode(TypeNode):
    """
    Resolved Type Node: Pointer

    Represents an address pointing to a target TypeNode.
    """
    # -Properties
    target: TypeNode

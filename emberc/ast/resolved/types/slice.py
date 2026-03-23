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
class SliceTypeNode(TypeNode):
    """
    Resolved Type Node: Slice

    Represents a view into a contigious sequence of a target TypeNode.
    Can represent either a managed fat-pointer or a raw pointer.
    """
    # -Properties
    target: TypeNode
    is_raw: bool

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type Node: Slices             ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from .base import NodeType


## Classes
@dataclass(frozen=True, slots=True)
class NodeTypeSlice(NodeType):
    """
    Ember Type: Slice

    A type representing a slice to a target type
    """
    # -Properties
    many_to_one: bool
    target: NodeType

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type Node: Pointer            ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from .base import NodeType


## Classes
@dataclass(frozen=True, slots=True)
class NodeTypePointer(NodeType):
    """
    Ember Type: Pointer

    A type representing a pointer to a target type
    """
    # -Properties
    target: NodeType

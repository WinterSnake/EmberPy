##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type Node: Function           ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .base import NodeType

if TYPE_CHECKING:
    from collections.abc import Collection


## Classes
@dataclass(frozen=True, slots=True)
class NodeTypeFunction(NodeType):
    """
    Ember Type: Function

    A type representing the function signature (return + parameters)
    """
    # -Properties
    return_type: NodeType
    parameter_types: Collection[NodeType]

    @property
    def arity(self) -> int:
        return len(parameter_types)

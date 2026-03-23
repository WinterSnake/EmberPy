##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type Node: Function           ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .core import TypeNode

if TYPE_CHECKING:
    from ....core import MutableCollection


## Classes
@dataclass(frozen=True, slots=True)
class FunctionTypeNode(TypeNode):
    """
    Resolved Type Node: Function

    Represents a function's signature with the return type and it's parameter types.
    """
    # -Properties
    return_type: TypeNode
    parameter_types: MutableCollection[TypeNode]

    @property
    def arity(self) -> int:
        return len(self.parameter_types)

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type Node: Identifier         ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from .core import TypeNode


## Classes
@dataclass(slots=True)
class EnumTypeNode(TypeNode):
    """
    Resolved Type Node: Enum

    """
    # -Properties
    underlying: TypeNode

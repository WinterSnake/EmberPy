##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type Node: Enum               ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from .core import TypeNode


## Classes
@dataclass(slots=True)
class EnumTypeNode(TypeNode):
    """
    Resolved Type Node: Enum
 
    A reference to a user-defined enum; enum vs tagged enum are defined
    within the symbol table and its member's symbols.
    """
    # -Properties
    underlying: TypeNode

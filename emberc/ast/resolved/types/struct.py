##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Type Node: Struct             ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from .core import TypeNode


## Classes
@dataclass(frozen=True, slots=True)
class StructTypeNode(TypeNode):
    """
    Resolved Type Node: Struct
    
    A semantic marker identifying a symbol as a structured data type.
    """
    pass

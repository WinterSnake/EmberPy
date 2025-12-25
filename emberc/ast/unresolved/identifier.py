##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Identifier   ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from .node import UnresolvedNode


## Classes
@dataclass
class UnresolvedIdentifierNode(UnresolvedNode):
    """
    Ember Unresolved Node: Identifier

    A node for storing an identifier's name
    """
    # -Properties
    name: str

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node                          ##
##-------------------------------##

## Imports
from abc import ABC, abstractmethod
from ...location import Location


## Classes
class NodeBase(ABC):
    """
    Ember Node
    Base class for all AST Nodes
    """

    # -Constructor
    def __init__(self, location: Location) -> None:
        self.location: Location = location

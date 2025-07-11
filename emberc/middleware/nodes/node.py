##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node                          ##
##-------------------------------##

## Imports
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from .visitor import NodeVisitor
from ...location import Location


## Classes
class Node(ABC):
    """
    """

    # -Constructor
    def __init__(self, location: Location) -> None:
        self.location: Location = location

    # -Instance Methods
    @abstractmethod
    def accept(self, visitor: NodeVisitor) -> Any: ...

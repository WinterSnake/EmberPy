#!/usr/bin/python
##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Frontend: Node                ##
##-------------------------------##

## Imports

## Constants
__all__: tuple[str] = ("Node",)


## Classes
class Node:
    """"""

    # -Constructor
    def __init__(self, name: str) -> None:
        self.name: str = name

    # -Dunder Methods
    def __repr(self) -> str:
        return f"Node(name={self.name})"

    def __str__(self) -> str:
        return f"Function[{self.name}]"

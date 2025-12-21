##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Statement               ##
##-------------------------------##

## Imports
from .node import NodeBase
from ...location import Location


## Classes
class NodeStmt(NodeBase):
    """
    Ember Statement Node
    Represents an AST node of a statement
    """

    # -Constructor
    def __init__(self, location: Location) -> None:
        super().__init__(location)

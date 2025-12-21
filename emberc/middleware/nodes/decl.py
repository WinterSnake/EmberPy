##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Declaration             ##
##-------------------------------##

## Imports
from .node import NodeBase
from ...location import Location


## Classes
class NodeDecl(NodeBase):
    """
    Ember Declaration Node
    Represents an AST node of a declaration
    """

    # -Constructor
    def __init__(self, location: Location) -> None:
        super().__init__(location)

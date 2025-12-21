##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Expression              ##
##-------------------------------##

## Imports
from .node import NodeBase
from ...location import Location


## Classes
class NodeExpr(NodeBase):
    """
    Ember Expression Node
    Represents an AST node of an expression
    """

    # -Constructor
    def __init__(self, location: Location) -> None:
        super().__init__(location)

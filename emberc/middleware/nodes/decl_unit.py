##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Node: Declaration Unit        ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Collection
from .node import NodeBase
from .decl import NodeDecl
from ...location import Location


## Classes
class NodeDeclUnit(NodeDecl):
    """
    Ember Declaration Node : Unit
    Represents an AST node of a compilation unit
    """

    # -Constructor
    def __init__(self, body: Collection[NodeBase]) -> None:
        self.body: Collection[NodeBase] = body

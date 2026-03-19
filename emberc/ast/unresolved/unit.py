##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Unit         ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from typing import MutableSequence


## Classes
@dataclass
class UnresolvedUnitNode(UnresolvedNode):
    """
    Unresolved AST Node: Unit

    A top-level container for a unit for files or modules.
    Holds a mutable sequence of root nodes.
    """
    # -Properties
    nodes: MutableSequence[UnresolvedNode]

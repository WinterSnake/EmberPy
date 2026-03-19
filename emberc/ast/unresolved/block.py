##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Block        ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from typing import MutableSequence


## Classes
@dataclass
class UnresolvedBlockNode(UnresolvedNode):
    """
    Unresolved AST Node: Block

    Represents a sequence of statements enclosed within curly braces '{ }'.
    """
    # -Properties
    nodes: MutableSequence[UnresolvedNode]

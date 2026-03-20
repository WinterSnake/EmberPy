##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node               ##
##-------------------------------##

## Imports
from abc import ABC
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import MutableSequence
    from ...core import Location


## Classes
@dataclass
class UnresolvedNode(ABC):
    """
    Unresolved AST Node

    An abstract base for all structural AST nodes produced by the parser.
    """
    # -Properties
    location: Location


@dataclass
class UnresolvedUnitNode(UnresolvedNode):
    """
    Unresolved AST Node: Unit

    A top-level container for a unit for files or modules.
    Holds a mutable sequence of root nodes.
    """
    # -Properties
    nodes: MutableSequence[UnresolvedNode]

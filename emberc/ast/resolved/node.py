##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Resolved Node                 ##
##-------------------------------##

## Imports
from abc import ABC
from dataclasses import dataclass


## Classes
class ResolvedNode(ABC):
    """
    Resolved AST Node

    An abstract base for all structural AST nodes produced after
    lowering the unresolved AST tree. This set of nodes holds 0 ambiguity.
    """
    pass

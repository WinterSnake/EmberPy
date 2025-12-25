##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Group        ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from .node import UnresolvedNode


## Classes
@dataclass
class UnresolvedGroupNode(UnresolvedNode):
    """
    Ember Unresolved Node: Group

    A node for storing a grouped expression and optional target
    where target could be a potential greedy cast or binary operation
    """
    # -Properties
    inner: UnresolvedNode
    _target: UnresolvedNode | None = None

    @property
    def has_target(self) -> bool:
        return self._target is not None

    @property
    def target(self) -> UnresolvedNode:
        assert self._target is not None
        return self._target

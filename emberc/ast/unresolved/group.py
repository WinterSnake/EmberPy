##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Group        ##
##-------------------------------##

## Imports
from __future__ import annotations
from dataclasses import dataclass
from .node import UnresolvedNode


## Classes
@dataclass
class UnresolvedGroupNode(UnresolvedNode):
    """
    Unresolved AST Node: Group

    A container for a grouped expression and optional target.
    Target is applied when an ambiguity arises between operators and grouping.
    """
    # -Properties
    inner: UnresolvedNode
    _target: UnresolvedNode | None = None

    @property
    def has_target(self) -> bool:
        return self._target is not None

    @property
    def target(self) -> UnresolvedNode:
        assert self._target is not None, "TODO: Error handling"
        return self._target


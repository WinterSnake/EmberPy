##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Conditional  ##
##-------------------------------##

## Imports
from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum, auto
from .node import UnresolvedNode


## Classes
@dataclass
class UnresolvedWhileNode(UnresolvedNode):
    """
    Unresolved AST Node: Loop-While

    Represents a while loop with a entry-condition and a body.
    """
    # -Properties
    condition: UnresolvedNode
    body: UnresolvedNode


@dataclass
class UnresolvedDoNode(UnresolvedNode):
    """
    Unresolved AST Node: Loop-Do

    Represents a do-while loop with a body and an exit-condition.
    """
    # -Properties
    condition: UnresolvedNode
    body: UnresolvedNode


@dataclass
class UnresolvedForNode(UnresolvedNode):
    """
    Unresolved AST Node: Loop-For

    Represents a for loop with optional initializer, condition, and increment.
    """
    # -Properties
    _initializer: UnresolvedNode | None
    condition: UnresolvedNode
    _increment: UnresolvedNode | None
    body: UnresolvedNode

    @property
    def has_initializer(self) -> bool:
        return self._initializer is not None

    @property
    def initializer(self) -> UnresolvedNode:
        assert self._initializer is not None
        return self._initializer

    @property
    def has_increment(self) -> bool:
        return self._increment is not None

    @property
    def increment(self) -> UnresolvedNode:
        assert self._increment is not None
        return self._increment


@dataclass
class UnresolvedFlowNode(UnresolvedNode):
    """
    Unresolved AST Node: Flow

    ...
    """
    # -Properties
    kind: UnresolvedFlowNode.Kind

    # -Sub-Classes
    class Kind(IntEnum):
        Break = auto()
        Continue = auto()

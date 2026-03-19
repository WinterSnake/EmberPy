##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Conditional  ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from typing import MutableSequence


## Classes
@dataclass
class UnresolvedConditionalNode(UnresolvedNode):
    """
    Unresolved AST Node: Conditional

    Represents an 'if-else' control flow structure with conditional expression.
    """
    # -Properties
    condition: UnresolvedNode
    if_branch: UnresolvedNode
    _else_branch: UnresolvedNode | None

    @property
    def has_else_branch(self) -> bool:
        return self._else_branch is not None

    @property
    def else_branch(self) -> UnresolvedNode:
        assert self._else_branch is not None
        return self._else_branch

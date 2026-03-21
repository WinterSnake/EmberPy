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
    from ...core import Location, MutableCollection


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


@dataclass
class UnresolvedSwitchNode(UnresolvedNode):
    """
    Unresolved AST Node: Switch

    Represents a 'switch' control flow structure with case expressions and bodies.
    """
    # -Properties
    condition: UnresolvedNode
    groups: MutableCollection[UnresolvedSwitchNode.Group]
    _default: UnresolvedNode | None

    @property
    def has_default(self) -> bool:
        return self._default is not None

    @property
    def default(self) -> UnresolvedNode:
        assert self._default is not None
        return self._default

    # -Sub-Classes
    @dataclass
    class Case:
        '''Meta-data for switch case entries'''
        # -Properties
        location: Location
        condition: UnresolvedNode

    @dataclass
    class Group:
        '''Meta-data for switch case groups (a collection of cases)'''
        # -Properties
        cases: list[UnresolvedSwitchNode.Case]
        body: UnresolvedNode

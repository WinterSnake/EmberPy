##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Declaration  ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Collection
from dataclasses import dataclass
from typing import TYPE_CHECKING
from .node import UnresolvedNode
from ...location import Location

if TYPE_CHECKING:
    from .statement import UnresolvedStmtNode


## Classes
@dataclass
class UnresolvedDeclNode(UnresolvedNode):
    """
    Ember Unresolved Node: Declaration

    A base node for storing declaration context
    """
    pass


@dataclass
class UnresolvedDeclFunctionNode(UnresolvedDeclNode):
    """
    Ember Unresolved Declaration: Function

    A declaration for a function containing a name, parameters, return type, and body
    """
    # -Properties
    name: str
    parameters: Collection[UnresolvedDeclFunctionNode.Parameter]
    type: UnresolvedNode
    body: UnresolvedStmtNode

    @property
    def arity(self) -> int:
        return len(self.parameters)

    # -Sub-Classes
    @dataclass
    class Parameter:
        '''Meta-data for function parameters'''
        # -Properties
        type: UnresolvedNode
        name: str
        _initializer: UnresolvedNode | None

        @property
        def location(self) -> Location:
            return self.type.location

        @property
        def has_initializer(self) -> bool:
            return self._initializer is not None

        @property
        def initializer(self) -> UnresolvedNode:
            assert self._initializer is not None
            return self._initializer


@dataclass
class UnresolvedDeclVariableNode(UnresolvedDeclNode):
    """
    Ember Unresolved Declaration: Variable

    A declaration for a variable containing a type and collection of entries
    """
    # -Properties
    type: UnresolvedNode
    entries: Collection[UnresolvedDeclVariableNode.Entry]
    # -Sub-Classes
    @dataclass
    class Entry:
        '''Meta-data for variable entries'''
        # -Properties
        location: Location
        name: str
        _initializer: UnresolvedNode | None

        @property
        def has_initializer(self) -> bool:
            return self._initializer is not None

        @property
        def initializer(self) -> UnresolvedNode:
            assert self._initializer is not None
            return self._initializer

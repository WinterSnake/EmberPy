##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Declaration  ##
##-------------------------------##

## Imports
from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from collections.abc import Collection
    from .statement import UnresolvedStmtNode
    from ...location import Location


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
    id: int = field(init=False, repr=False)

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
        id: int = field(init=False, repr=False)

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
class UnresolvedDeclEnumNode(UnresolvedDeclNode):
    """
    Ember Unresolved Declaration: Enum

    A declaration for an enum containing a type and collection of entries
    """
    # -Properties
    name: str
    _type: UnresolvedNode | None
    entries: Collection[UnresolvedDeclEnumNode.Entry]

    @property
    def has_type(self) -> bool:
        return self._type is not None

    @property
    def type(self) -> UnresolvedNode:
        assert self._type is not None
        return self._type

    # -Sub-Classes
    @dataclass
    class Entry:
        '''Meta-data for enum entries'''
        # -Properties
        location: Location
        name: str
        _initializer: UnresolvedNode | None
        id: int = field(init=False, repr=False)

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
        id: int = field(init=False, repr=False)

        @property
        def has_initializer(self) -> bool:
            return self._initializer is not None

        @property
        def initializer(self) -> UnresolvedNode:
            assert self._initializer is not None
            return self._initializer

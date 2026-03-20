##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Unresolved Node: Variable     ##
##-------------------------------##

## Imports
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from .node import UnresolvedNode

if TYPE_CHECKING:
    from ...core import Location, MutableCollection


## Classes
@dataclass
class UnresolvedFunctionNode(UnresolvedNode):
    """
    Unresolved AST Node: Function

    Represents a function definition including parameters, return type, and body.
    """
    # -Properties
    name: str
    _id: int | None = field(init=False, default=None)
    parameters: MutableCollection[UnresolvedFunctionNode.Parameter]
    return_type: UnresolvedNode
    body: UnresolvedNode

    @property
    def has_id(self) -> bool:
        return self._id is not None

    @property
    def id(self) -> int:
        assert self._id is not None
        return self._id

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
        _id: int | None = field(init=False, default=None)
        _initializer: UnresolvedNode | None

        @property
        def has_id(self) -> bool:
            return self._id is not None

        @property
        def id(self) -> int:
            assert self._id is not None
            return self._id

        @property
        def has_initializer(self) -> bool:
            return self._initializer is not None

        @property
        def initializer(self) -> UnresolvedNode:
            assert self._initializer is not None
            return self._initializer


@dataclass
class UnresolvedReturnNode(UnresolvedNode):
    """
    Unresolved AST Node: Return

    A container for a return statement with an optional expression value.
    """
    # -Properties
    _expression: UnresolvedNode | None

    @property
    def has_expression(self) -> bool:
        return self._expression is not None

    @property
    def expression(self) -> UnresolvedNode:
        assert self._expression is not None, "TODO: Error handling"
        return self._expression

##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Interpreter: Environment      ##
##-------------------------------##

## Imports
from dataclasses import dataclass, field
from typing import ClassVar, Self

## Constants
type INTERPRETER_VALUE = int
type Scope = dict[int, INTERPRETER_VALUE | None]

## Classes
@dataclass(slots=True)
class Environment:
    """
    Manages runtime variable state using a stack of lexical scopes.
    
    Provides scoping mechanisms (push/pop) and variable operations (declaration, 
    lookup, and assignment) that bubble up through the scope hierarchy.
    """

    # -Dunder Methods
    def __getitem__(self, _id: int) -> INTERPRETER_VALUE:
        '''Retrieve value of variable by bubbling up scopes'''
        for scope in reversed(self._scopes):
            if _id not in scope:
                continue
            value = scope[_id]
            assert value is not None
            return value
        assert False, f"Tried to retrieve value from unknown id[{_id}]"

    # -Instance Methods: Scope
    def push(self) -> None:
        self._scopes.append(dict())

    def pop(self) -> Scope:
        return self._scopes.pop()

    # -Instance Methods: Values
    def declare(self, _id: int, value: INTERPRETER_VALUE | None) -> None:
        '''Declare variable in current scope'''
        self.current_scope[_id] = value

    def assign(self, _id: int, value: INTERPRETER_VALUE) -> None:
        '''Assign value to variable by bubbling up scopes'''
        for scope in reversed(self._scopes):
            if _id not in scope:
                continue
            scope[_id] = value
            return
        assert False, f"Tried to assign value to unknown id[{_id}]"

    # -Properties
    _scopes: list[Scope] = field(default_factory=lambda: [{}])

    @property
    def current_scope(self) -> Scope:
        return self._scopes[-1]

    # -Class Properties
    default: ClassVar[Self]


## Body
Environment.default = Environment()

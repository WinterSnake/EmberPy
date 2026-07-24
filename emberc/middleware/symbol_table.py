##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Middleware: Symbol Table      ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence
    from ..ast import TypeNode

## Constants
type Scope = dict[str, int]


## Classes
@dataclass(slots=True)
class Symbol:
    """
    Ember Symbol

    Foundation for name identity, including: id, symbol variant, and value type.
    """
    # -Properties
    id: int
    name: str
    kind: Symbol.Kind
    type: TypeNode

    # -Sub-Classes
    class Kind(IntEnum):
        Variable = auto()


class SymbolTable:
    """Maps a collection of symbols to unique ids. Handles scope creation and searching."""
    # -Constructor
    def __init__(self) -> None:
        self._scopes: list[Scope] = [{}]
        self._symbols: list[Symbol] = []

    # -Instance Methods: Symbol
    def add_symbol(
        self, name: str, kind: Symbol.Kind, _type: TypeNode
    ) -> int | None:
        '''Create symbol and return id or None if symbol already exists.'''
        if name in self.current_scope:
            return None
        _id = self.next_id
        self._symbols.append(Symbol(_id, name, kind, _type))
        self.current_scope[name] = _id
        return _id

    def find_id(self, name: str) -> int | None:
        '''Find and return symbol id by bubbling up scopes from top-down or None if non-existent.'''
        for scope in reversed(self._scopes):
            if name in scope:
                return scope[name]
        return None

    def find_id_local(self, name: str) -> int | None:
        '''Find and return symbol id within current scopet or None if non-existent.'''
        return self.current_scope.get(name, None)

    # -Instance Methods: Table
    def push(self) -> None:
        '''Push new scope onto the stack.'''
        self._scopes.append({})

    def pop(self) -> Scope:
        '''Pop and return scope from the stack.'''
        return self._scopes.pop()

    # -Instance Methods: Helpers
    def add_variable(self, name: str, _type: TypeNode) -> int | None:
        '''Route and return symbol creation with variable hinting.'''
        return self.add_symbol(name, Symbol.Kind.Variable, _type)

    # -Properties
    @property
    def next_id(self) -> int:
        return len(self._symbols)

    @property
    def current_scope(self) -> Scope:
        '''Return top-level scope.'''
        return self._scopes[-1]

    @property
    def scope_depth(self) -> int:
        '''Return current scope depth.'''
        return len(self._scopes) - 1

    @property
    def symbols(self) -> Sequence[Symbol]:
        '''Return symbol collection from table.'''
        assert self.scope_depth == 0, "Tried getting symbols on non-rooted table."
        self._scopes.clear()
        return tuple(self._symbols)

    # -Class Properties
    __slots__ = ("_scopes", "_symbols")

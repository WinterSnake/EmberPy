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
    Represents a uniquely identified entity resolved by the compiler.
    
    Tracks identity, lexical identifier name, definition variant (kind), 
    and the concrete evaluation type of a compiler primitive.
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
    """
    Manages lexical scopes and unique symbol assignments during compilation.
    
    Provides a block-structured environment for looking up variable 
    identities, managing stacked variable scopes, and enforcing symbol isolation.
    """

    # -Constructor
    def __init__(self) -> None:
        self._symbols: list[Symbol] = []
        self._scopes: list[Scope] = [{}]

    # -Instance Methods
    def add_symbol(self, name: str, kind: Symbol.Kind, _type: TypeNode) -> int | None:
        '''
        Creates a symbol and appends it to current scope.
        Returns None when symbol already exists
        '''
        if name in self.current_scope:
            return None
        idx = len(self._symbols)
        self._symbols.append(Symbol(idx, name, kind, _type))
        self.current_scope[name] = idx
        return idx

    def find_id(self, name: str) -> int | None:
        '''Finds and returns symbol id by bubbling up scopes from top down'''
        for scope in reversed(self._scopes):
            if name in scope:
                return scope[name]
        return None

    def find_local_id(self, name: str) -> int | None:
        '''Finds and returns symbol id for current scope or None if non-existent'''
        return self.current_scope.get(name, None)

    # -Instance Methods: Helpers
    def add_variable(self, name: str, _type: TypeNode) -> int | None:
        '''Routes variable declaration into add_symbol'''
        return self.add_symbol(name, Symbol.Kind.Variable, _type)

    # -Properties
    @property
    def current_scope(self) -> Scope:
        return self._scopes[-1]

    @property
    def scope_depth(self) -> int:
        return len(self._scopes) - 1

    @property
    def symbols(self) -> Sequence[Symbol]:
        return tuple(self._symbols)

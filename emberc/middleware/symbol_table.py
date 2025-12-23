##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Middleware: Symbol Table      ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from .nodes import NodeType


## Classes
class Symbol:
    """
    Ember Symbol

    Contains metadata for types, identifiers, and general node structures
    """

    # -Constructor
    def __init__(
        self, _id: int, name: str, kind: Symbol.Kind, _type: NodeType
    ) -> None:
        self.id: int = _id
        self.name: str = name

    # -Dunder Methods
    def __str__(self) -> str:
        return f"Symbol[{self.id}; {self.name}]"

    # -Sub-Classes
    class Kind(IntEnum):
        Function = auto()
        Variable = auto()


class SymbolTable:
    """
    Ember Symbol Table

    A table of symbols for handling creating scoped ids and bubbling up lookup
    After finalized, becomes a (mostly) readonly table of lookups
    """

    # -Constructor
    def __init__(self) -> None:
        self._scopes: list[dict[str, int]] = [{}]
        self._symbols: list[Symbol] = []

    # -Dunder Methods
    def __str__(self) -> str:
        return '[' + ','.join(str(symbol) for symbol in self._symbols) + ']'

    # -Instance Methods
    def push(self) -> None:
        self._scopes.append({})

    def pop(self, is_final: bool = False) -> None:
        if len(self._scopes) <= 1 and not is_final:
            raise RuntimeError("Tried popping global scope before final call")
        self._scopes.pop()

    def add(self, name: str, kind: Symbol.Kind, _type: NodeType) -> int | None:
        '''Adds a symbol to the current scope and returns index into flat table'''
        if name in self.current_scope:
            return None
        index = len(self._symbols)
        symbol = Symbol(index, name, kind, _type)
        self._symbols.append(symbol)
        self.current_scope[name] = index
        return index

    def get(self, index: int) -> Symbol:
        '''Readonly operation: returns the symbol from id for node passes'''
        return self._symbols[index]

    def find(self, name: str) -> int | None:
        '''Finds the current name by bubbling up through scopes'''
        for scope in reversed(self._scopes):
            if name in scope:
                return scope[name]
        return None

    # -Properties
    @property
    def current_scope(self) -> dict[str, int]:
        return self._scopes[-1]

    @property
    def scope_depth(self) -> int:
        return len(self._scopes) - 1

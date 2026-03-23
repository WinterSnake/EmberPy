##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Middleware: Symbol Table      ##
##-------------------------------##

## Imports
from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import TYPE_CHECKING
from ..ast import (
    PendingTypeNode,
    StructTypeNode,
    FunctionTypeNode,
)

if TYPE_CHECKING:
    from collections.abc import Sequence
    from ..ast import TypeNode
    from ..core import MutableCollection

## Constants
type SCOPE = dict[str, int]


## Classes
@dataclass(slots=True)
class Symbol:
    """A unique semantic record representing a named entity"""
    # -Properties
    id: int
    name: str
    type: TypeNode
    kind: Symbol.Kind

    # -Sub-Classes
    class Kind(IntEnum):
        Struct = auto()
        Enum = auto()
        EnumMember = auto()
        TaggedEnum = auto()
        EnumVariant = auto()
        Function = auto()
        Parameter = auto()
        Variable = auto()


class SymbolTable:
    """
    The central repository for name resolution and scope management.
    It maps identifiers to Symbol records and maintains the lexical stack
    to ensure correct visibility and prevent redefinitions.
    """

    # -Constructor
    def __init__(self) -> None:
        self._symbols: list[Symbol] = []
        self._scopes: list[SCOPE] = [{}]
        self._member_scopes: dict[int, SCOPE] = {}

    # -Instance Methods
    def add_symbol(
        self, name: str, kind: Symbol.Kind, _type: TypeNode
    ) -> int | None:
        '''Adds a symbol to the current scope and returns index into flat table'''
        if name in self.current_scope:
            return None
        idx = len(self._symbols)
        self.current_scope[name] = idx
        self._symbols.append(Symbol(idx, name, _type, kind))
        return idx

    def add_member_symbol(
        self, parent: int, name: str, kind: Symbol.Kind, _type: TypeNode
    ) -> int | None:
        '''Adds a symbol to a parent's scope and returns index into flat table'''
        if (scope := self._member_scopes.get(parent, None)) is None:
            return None
        if name in scope:
            return None
        idx = len(self._symbols)
        scope[name] = idx
        self._symbols.append(Symbol(idx, name, _type, kind))
        return idx

    def find_id(self, name: str) -> int | None:
        '''Finds the given name by bubbling up through scopes'''
        for scope in reversed(self._scopes):
            if name in scope:
                return scope[name]
        return None

    def find_local_id(self, name: str) -> int | None:
        '''Finds the given name within the local scope'''
        return self.current_scope.get(name, None)

    def find_member_id(self, parent: int, name: str) -> int | None:
        '''Find the given name within a parent's scope'''
        if (scope := self._member_scopes.get(parent, None)) is None:
            return None
        return scope.get(name, None)

    # -Instance Methods: Helpers
    def add_struct(self, name: str) -> int | None:
        if (_id := self.add_symbol(name, Symbol.Kind.Struct, StructTypeNode())) is None:
            return None
        self._member_scopes[_id] = {}
        return _id

    def add_enum(
        self, name: str, _type: TypeNode, is_tagged: bool
    ) -> int | None:
        kind = Symbol.Kind.TaggedEnum if is_tagged else Symbol.Kind.Enum
        if (_id := self.add_symbol(name, kind, _type)) is None:
            return None
        self._member_scopes[_id] = {}
        return _id

    def add_enum_member(
        self, parent: int, name: str, is_tagged: bool
    ) -> int | None:
        kind = Symbol.Kind.EnumVariant if is_tagged else Symbol.Kind.EnumMember
        return self.add_member_symbol(
            parent, name, kind, PendingTypeNode(parent)
        )

    def add_function(
        self, name: str, return_type: TypeNode,
        parameter_types: MutableCollection[TypeNode]
    ) -> int | None:
        return self.add_symbol(
            name, Symbol.Kind.Function,
            FunctionTypeNode(return_type, parameter_types)
        )

    def add_variable(self, name: str, _type: TypeNode) -> int | None:
        return self.add_symbol(name, Symbol.Kind.Variable, _type)

    # -Properties
    @property
    def current_scope(self) -> dict[str, int]:
        return self._scopes[-1]

    @property
    def symbols(self) -> Sequence[Symbol]:
        return tuple(self._symbols)

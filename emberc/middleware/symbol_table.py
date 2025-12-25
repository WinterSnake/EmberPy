##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Middleware: Symbol Table      ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum, auto
from typing import TYPE_CHECKING
from ..ast import NodeTypeFunction

if TYPE_CHECKING:
    from collections.abc import Collection, Sequence
    from ..ast import NodeType

## Constants
type Symbols = Sequence[Symbol]


## Classes
class Symbol:
    """
    Ember Symbol

    Contains metadata for types, identifiers, and general node usage
    """

    # -Constructor
    def __init__(
        self, _id: int, name: str, kind: Symbol.Kind, _type: NodeType | None
    ) -> None:
        self.id: int = _id
        self.name: str = name
        self.kind: Symbol.Kind = kind
        self._type: NodeType | None = _type

    # -Dunder Methods
    def __str__(self) -> str:
        return f"[Symbol({self.id}:{self.name}); kind={self.kind.name}]"

    # -Properties
    @property
    def type(self) -> NodeType:
        assert self._type is not None
        return self._type

    # -Sub-Classes
    class Kind(IntEnum):
        Function = auto()
        Parameter = auto()
        Variable = auto()


class SymbolTable:
    """
    Ember Symbol Table

    Used to create a table of symbols for binding while walking the AST tree
    After finalized, becomes a readonly array of symbols, where ids are index
    """

    # -Constructor
    def __init__(self, parent: SymbolTable | None = None) -> None:
        self._symbols: list[Symbol] = []
        self._scopes: list[dict[str, int]] = []
        if parent is not None:
            assert parent.scope_depth == 0
            self._symbols.extend(parent._symbols)
            self._scopes.append(parent.root_scope)
        else:
            self._scopes.append({})

    # -Instance Methods
    def push(self) -> None:
        self._scopes.append({})

    def pop(self, is_final: bool = False) -> dict[str, int]:
        if self.scope_depth == 0 and not is_final:
            raise RuntimeError("Tried popping parent scope in non-final block")
        return self._scopes.pop()

    def add(
        self, name: str, kind: Symbol.Kind, _type: NodeType | None
    ) -> int | None:
        '''Adds a symbol to the current scope and returns index into flat table'''
        if name in self.current_scope:
            return None
        index = len(self._symbols)
        symbol = Symbol(index, name, kind, _type)
        self._symbols.append(symbol)
        self.current_scope[name] = index
        return index

    def add_function(
        self, name: str, _type: NodeType, parameters: Collection[NodeType]
    ) -> int | None:
        _type = NodeTypeFunction(_type, parameters)
        return self.add(name, Symbol.Kind.Function, _type)

    def add_variable(self, name: str, _type: NodeType) -> int | None:
        return self.add(name, Symbol.Kind.Variable, _type)

    def assign_type(self, _id: int, _type: NodeType) -> None:
        symbol = self._symbols[_id]
        symbol._type = _type

    def find_local(self, name: str) -> int | None:
        '''Finds the given name within the current scope'''
        return self.current_scope.get(name, None)

    def find(self, name: str) -> int | None:
        '''Finds the given name by bubbling up through scopes'''
        for scope in reversed(self._scopes):
            if name in scope:
                return scope[name]
        return None

    # -Properties
    @property
    def root_scope(self) -> dict[str, int]:
        return self._scopes[0]

    @property
    def current_scope(self) -> dict[str, int]:
        return self._scopes[-1]

    @property
    def scope_depth(self) -> int:
        return len(self._scopes) - 1

    @property
    def symbols(self) -> Symbols:
        return tuple(self._symbols)

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
from ..ast import FunctionTypeNode

if TYPE_CHECKING:
    from ..ast import TypeNode
    from ..core import MutableCollection


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
        self._scopes: list[dict[str, int]] = [{}]

    # -Instance Methods
    def add_symbol(
        self, name: str, kind: Symbol.Kind, _type: TypeNode
    ) -> int | None:
        if name in self.current_scope:
            return None
        idx = len(self._symbols)
        self.current_scope[name] = idx
        self._symbols.append(Symbol(idx, name, _type, kind))
        return idx

    # -Instance Methods: Helpers
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

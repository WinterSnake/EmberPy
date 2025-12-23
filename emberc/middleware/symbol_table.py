##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Middleware: Symbol Table      ##
##-------------------------------##

## Classes
class Symbol:
    """
    Ember Symbol

    Contains metadata for types, identifiers, and general node structures
    """

    # -Constructor
    def __init__(self, _id: int, name: str) -> None:
        self.id: int = _id
        self.name: str = name


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

    # -Instance Methods
    def push(self) -> None:
        self._scopes.append({})

    def pop(self, is_final: bool = False) -> None:
        if len(self._scopes) <= 1 and not is_final:
            raise RuntimeError("Tried popping global scope before final call")
        self._scopes.pop()

    def add(self, name: str) -> int | None:
        '''Adds a symbol to the current scope and returns index into flat table'''
        if name in self.current_scope:
            return None
        index = len(self._symbols)
        symbol = Symbol(index, name)
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

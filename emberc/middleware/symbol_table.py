##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Symbol Table                  ##
##-------------------------------##

## Imports
from __future__ import annotations
from .datatype import Datatype


## Classes
class SymbolTable:
    """
    Symbol Table

    Stores identifier information for lookup through other passes
    """

    # -Constructor
    def __init__(self) -> None:
        self.entries: list[SymbolTable.Entry] = []

    # -Instance Methods
    def add(self, name: str, _type: Datatype) -> int:
        index: int
        index = self.get(name)
        if index >= 0:
            return index
        index = len(self.entries)
        entry = SymbolTable.Entry(name, _type)
        self.entries.append(entry)
        return index

    def get(self, name: str) -> int:
        for i, entry in enumerate(self.entries):
            if entry.name == name:
                return i
        return -1

    def lookup(self, index: int) -> SymbolTable.Entry:
        return self.entries[index]

    # -Sub-Classes
    class Entry:

        # -Constructor
        def __init__(self, name: str, _type: Datatype) -> None:
            self.name: str = name
            self.type: Datatype = _type

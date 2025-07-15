##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Symbol Table                  ##
##-------------------------------##


## Classes
class SymbolTable:
    """
    Symbol Table

    Stores identifier information for lookup through other passes
    """

    # -Constructor
    def __init__(self) -> None:
        self.entries: list[str] = []

    # -Instance Methods
    def add(self, name: str) -> int:
        index: int
        index = self.get(name)
        if index >= 0:
            return index
        index = len(self.entries)
        self.entries.append(name)
        return index

    def get(self, name: str) -> int:
        for i, entry in enumerate(self.entries):
            if entry == name:
                return i
        return -1

    def lookup(self, index: int) -> str:
        return self.entries[index]

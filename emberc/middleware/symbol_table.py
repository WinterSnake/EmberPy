##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Symbo Table                   ##
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
        index: int = len(self.entries)
        self.entries.append(name)
        return index

    def get(self, name: str) -> int:
        for i, entry in enumerate(self.entries):
            if entry == name:
                return i
        return -1

    def lookup(self, index: int) -> str:
        return self.entries[index]

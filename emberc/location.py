##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Location                      ##
##-------------------------------##

## Imports
from pathlib import Path


## Classes
class Location:
    """Location for file and position"""

    # -Constructor
    def __init__(self, file: Path, position: tuple[int, int, int]) -> None:
        self.file: Path = file
        self.position: tuple[int, int, int] = position

    # -Dunder Methods
    def __str__(self) -> str:
        return f"[{self.file}:{self.row}:{self.column}:{self.offset}]"

    # -Properties
    @property
    def column(self) -> int:
        return self.position[1]

    @property
    def offset(self) -> int:
        return self.position[2]

    @property
    def row(self) -> int:
        return self.position[0]

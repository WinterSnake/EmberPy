##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Core: Location                ##
##-------------------------------##

## Imports
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


## Classes
@dataclass
class Location:
    """Source location for file and position"""

    # -Properties
    file: Path | None
    position: tuple[int, int, int]

    @property
    def column(self) -> int:
        return self.position[1]

    @property
    def offset(self) -> int:
        return self.position[2]

    @property
    def row(self) -> int:
        return self.position[0]

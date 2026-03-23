##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Core: Mutable Collection      ##
##-------------------------------##

## Imports
from collections.abc import Collection
from typing import Protocol


## Classes
class MutableCollection[T](Collection[T], Protocol):
    """A mutable fixed-sized ordered collection"""

    # -Dunder Methods
    def __getitem__(self, index: int) -> T: ...
    def __setitem__(self, index: int, value: T) -> None: ...

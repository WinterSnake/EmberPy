##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Diagnostics: Source Mapper    ##
##-------------------------------##

## Imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

## Classes
class SourceMap:
    """
    Maps source buffers to an id that is used throughout
    the entire lexing, parsing, and AST generation.
    """

    # -Constructor
    def __init__(self) -> None:
        self._map: dict[int, str] = {}
        self._files: dict[int, Path] = {}

    # -Instance Methods
    def _get_id(self) -> int:
        return len(self._map)

    def add_file(self, file: Path) -> int:
        with open(file, 'r') as f:
            source = f.read()
        _id = self.add_str(source)
        self._files[_id] = file
        return _id

    def add_str(self, source: str) -> int:
        _id = self._get_id()
        self._map[_id] = source
        return _id

    def is_file(self, _id: int) -> bool:
        return _id in self._files

    def get_file(self, _id: int) -> Path:
        return self._files[_id]

    def get_iter(self, _id: int) -> Iterator[str]:
        return iter(self._map[_id])

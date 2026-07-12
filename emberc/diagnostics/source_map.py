##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Diagnostic: Source Map        ##
##-------------------------------##

## Imports
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator


## Classes
class Source:
    """
    Represents a single source code input, either as an in-memory string or a file path.
    
    Provides an iterator over the source characters and acts as a central repository 
    for source-mapped metadata (like line offsets and comments) generated during lexing.
    """

    # -Constructor
    def __init__(self, _id: int, source: str | None, path: Path | None) -> None:
        self.id: int = _id
        self._source: str | None = source
        self._path: Path | None = path
        # -TODO: store lexed comments [generated from lexer]
        # -TODO: store indexable line offsets [generated from lexer]

    # -Instance Methods
    def get_iter(self) -> Iterator[str]:
        if self._source is None:
            if not self.is_path:
                raise ValueError("Source has neither a valid string nor a valid file path.")
            with self.path.open('r') as f:
                self._source = f.read()
        yield from self._source

    # -Properties
    @property
    def is_path(self) -> bool:
        return self._path is not None

    @property
    def path(self) -> Path:
        assert self._path is not None
        return self._path


class SourceMap:
    """
    A collection manager for tracking and indexing multiple `Source` inputs.
    
    Acts as a registry within the compiler to assign unique IDs to source files 
    or strings, enabling global lookups for diagnostics and error reporting.
    """

    # -Constructor
    def __init__(self) -> None:
        self._sources: list[Source] = []

    # -Dunder Methods
    def __getitem__(self, index: int) -> Source:
        return self._sources[index]

    def __iter__(self) -> Iterator[Source]:
        yield from self._sources

    def __len__(self) -> int:
        return len(self._sources)

    # -Instance Methods
    def add_str(self, source: str) -> int:
        _id = len(self._sources)
        self._sources.append(Source(_id, source, None))
        return _id

    def add_file(self, source: Path) -> int:
        _id = len(self._sources)
        self._sources.append(Source(_id, None, source))
        return _id

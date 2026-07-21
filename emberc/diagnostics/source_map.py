##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Diagnostics: Source Map       ##
##-------------------------------##

## Imports
import bisect
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import (
        Iterator,
        MutableSequence,
        Sequence,
    )
    from pathlib import Path
    from ..core import Span
    from ..frontend import Comment


## Classes
class Source:
    """
    Text Source

    Base foundation for raw string and file-based source code.
    """
    # -Constructor
    def __init__(self, text: str | None, path: Path | None) -> None:
        self._text: str | None = text
        self._path: Path | None = path
        self._comments: MutableSequence[Comment] = []
        self._line_offsets: MutableSequence[int] = [0]

    # -Instance Methods
    def get_text_iter(self) -> Iterator[str]:
        '''Return string iterator over source text; loading file if cached text is missing.'''
        if self._text is None:
            with self.path.open('r') as f:
                self._text = f.read()
        yield from self._text

    def resolve_location(self, position: int) -> tuple[int, int]:
        '''Return calculated (row, column) pair from given byte offset.'''
        row = bisect.bisect_right(self.line_offsets, position)
        column = (position - self.line_offsets[row - 1]) + 1
        return (row, column)

    # -Properties
    @property
    def text(self) -> str:
        '''Return source text; assert text is not None.'''
        assert self._text is not None
        return self._text

    @property
    def is_path(self) -> bool:
        '''Return if source is file-based.'''
        return self._path is not None

    @property
    def path(self) -> Path:
        '''Return path of source; assert path is not None.'''
        assert self._path is not None
        return self._path

    @property
    def comments(self) -> Sequence[Comment]:
        return tuple(self._comments)

    @property
    def line_offsets(self) -> Sequence[int]:
        return tuple(self._line_offsets)

    # -Class Properties
    __slots__ = (
        "_text",
        "_path",
        "_comments",
        "_line_offsets",
    )


class SourceMap:
    """Maps a collection of sources to unique ids."""
    # -Constructor
    def __init__(self) -> None:
        self._sources: MutableSequence[Source] = []

    # -Dunder Methods
    def __getitem__(self, index: int) -> Source:
        return self._sources[index]

    # -Instance Methods
    def add_str(self, source: str) -> int:
        '''Register string source to map and return assigned id.'''
        _id = self.next_id
        self._sources.append(Source(source, None))
        return _id

    def add_file(self, source: Path) -> int:
        '''Register file-based source to map and return assigned id.'''
        _id = self.next_id
        self._sources.append(Source(None, source))
        return _id

    def get_text_span(self, span: Span) -> str:
        '''Return text string from given span.'''
        return self._sources[span.id].text[span.start:span.end]

    # -Properties
    @property
    def next_id(self) -> int:
        return len(self._sources)

    # -Class Properties
    __slots__ = ("_sources",)

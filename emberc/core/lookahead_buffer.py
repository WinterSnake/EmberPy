##-------------------------------##
## Ember Compiler                ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Core: Lookahead Buffer        ##
##-------------------------------##

## Imports
from abc import ABC
from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

## Constants
__all__ = ("LookaheadBuffer",)
type Selector[Item, Key] = Callable[[Item], Key]


## Functions
def _get_key_from_item[Item, Key](
    item: Item, selector: Selector[Item, Key] | None
) -> Key:
    """Extract key from item using selector; return item as key if no selector."""
    if selector is not None:
        return selector(item)
    return item  # type: ignore[return-value]


## Classes
class LookaheadBuffer[Item, Key](ABC):
    """
    Lookahead(n) Buffer

    A base implementation for lookahead(n) streams.
    Specifically used for common logic between the lexer and parser.
    """
    # -Constructor
    def __init__(
        self, source: Iterator[Item],
        selector: Selector[Item, Key] | None = None
    ) -> None:
        self._source = source
        self._selector = selector
        self._buffer: deque[Item] = deque()
        self._is_at_end: bool = False

    # -Instance Methods
    def advance(self) -> Item | None:
        '''Advance the stream by one; return item or None if at end.'''
        if self.peek() is not None:
            return self._buffer.popleft()
        return None

    def peek(self, index: int = 0) -> Item | None:
        '''Peek at N item of stream; return None if index is out of bounds.'''
        if index < 0:
            raise IndexError("Tried peeking a negative amount in buffer")
        while len(self._buffer) <= index and not self._is_at_end:
            item = next(self._source, None)
            if item is None:
                self._is_at_end = True
                break
            self._buffer.append(item)
        if index < len(self._buffer):
            return self._buffer[index]
        return None

    def next(self) -> Item:
        '''Advance the stream by one; assert item exists and return it.'''
        item = self.advance()
        assert item is not None
        return item

    def consume(self, expected: Key) -> bool:
        '''Advance the stream by one if key matches expected; return if consumed.'''
        item = self.peek()
        if item is None:
            return False
        key = _get_key_from_item(item, self._selector)
        if key != expected:
            return False
        _ = self.advance()
        return True

    def matches(self, *expected: Key) -> bool:
        '''Check if next item's key matches expected keys; return if matching.'''
        item = self.peek()
        if item is None:
            return False
        key = _get_key_from_item(item, self._selector)
        return key in expected

    # -Properties
    @property
    def current(self) -> Item:
        '''Peek next item; assert item exists and return it.'''
        item = self.peek()
        assert item is not None
        return item

    @property
    def is_at_end(self) -> bool:
        '''Peek next item; return True if stream is exhausted and buffer empty.'''
        self.peek()
        return self._is_at_end and not self._buffer

    # -Class Properties
    __slots__ = (
        "_buffer",
        "_is_at_end",
        "_selector",
        "_source",
    )

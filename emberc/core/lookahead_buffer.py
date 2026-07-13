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
type TSelector[TItem, TKey] = Callable[[TItem], TKey]


## Functions
def _get_key_from_item[TItem, TKey](
    item: TItem, selector: TSelector[TItem, TKey] | None
) -> TKey:
    """
    Returns TKey either by assuming TKey is TItem
    or by calling the selector to get TKey from TItem
    """
    if selector is not None:
        return selector(item)
    return item  # type: ignore[return-value]


## Classes
class LookaheadBuffer[TItem, TKey](ABC):
    """
    Lookahead(n) Buffer

    A generic wrapper for iterators that provides arbitrary
    lookahead and item matching without premature consumption.
    """

    # -Constructor
    def __init__(
        self, source: Iterator[TItem],
        selector: TSelector[TItem, TKey] | None = None
    ) -> None:
        self._source: Iterator[TItem] = source
        self._selector: TSelector[TItem, TKey] | None = selector
        self._buffer: deque[TItem] = deque()
        self._is_at_end: bool = False

    # -Instance Methods
    def advance(self) -> TItem | None:
        '''Returns next TItem from buffer or source iterator; None if at end'''
        if self.peek() is not None:
            return self._buffer.popleft()
        return None

    def next(self) -> TItem:
        '''Returns next TItem; asserts TItem exists'''
        item = self.advance()
        assert item is not None
        return item

    def peek(self, index: int = 0) -> TItem | None:
        '''Fills buffer to N+1 TItem then returns buffer[N]; None if beyond source iterator'''
        if index < 0:
            raise IndexError(f"Tried to peek a negative amount ({index})")
        while len(self._buffer) <= index and not self._is_at_end:
            item = next(self._source, None)
            if item is None:
                self._is_at_end = True
            else:
                self._buffer.append(item)
        if index < len(self._buffer):
            return self._buffer[index]
        return None

    def consume(self, expected: TKey) -> bool:
        '''Returns boolean if next TItem is TKey; consumes'''
        value = self.peek()
        if value is None:
            return False
        key = _get_key_from_item(value, self._selector)
        if key != expected:
            return False
        _ = self.advance()
        return True

    def matches(self, *expected: TKey) -> bool:
        '''Returns boolean if next TItem in TKey; does not consume'''
        value = self.peek()
        if value is None:
            return False
        key = _get_key_from_item(value, self._selector)
        return key in expected

    # -Properties
    @property
    def current(self) -> TItem:
        '''Returns current TItem from iterator; asserts TItem exists'''
        item = self.peek()
        assert item is not None
        return item

    @property
    def is_at_end(self) -> bool:
        self.peek()
        return self._is_at_end and not self._buffer

    # -Class Properties
    __slots__ = ('_source', '_selector', '_buffer', '_is_at_end')
